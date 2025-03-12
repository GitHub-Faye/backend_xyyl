from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime
from .models import HealthRecord
from .serializers import HealthRecordSerializer


class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """获取用户的健康记录"""
        queryset = HealthRecord.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        try:
            if start_date:
                start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
                queryset = queryset.filter(record_time__date__gte=start_date.date())
            if end_date:
                end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                queryset = queryset.filter(record_time__date__lte=end_date.date())
        except ValueError as e:
            # 添加详细的错误日志
            print(f"日期格式错误: {e}")
            # 如果日期格式无效，返回空查询集
            return HealthRecord.objects.none()

        return queryset
    
    def _get_date_range_for_period(self, period):
        """根据时间周期计算日期范围"""
        today = timezone.now().date()
        if period == 'week':
            start_date = today - timezone.timedelta(days=7)
        elif period == 'month':
            start_date = today - timezone.timedelta(days=30)
        elif period == 'quarter':
            start_date = today - timezone.timedelta(days=90)
        else:  # 'all'
            start_date = None
        return start_date, today
    
    def _get_filtered_queryset(self, period, record_type):
        """获取根据时间周期和记录类型过滤的查询集"""
        start_date, today = self._get_date_range_for_period(period)
        
        # 构建基础查询
        queryset = self.get_queryset()
        if start_date:
            queryset = queryset.filter(record_time__date__gte=start_date)
        queryset = queryset.filter(record_time__date__lte=today)
        
        # 根据记录类型过滤
        if record_type == 'weight':
            queryset = queryset.exclude(weight__isnull=True)
        elif record_type == 'bloodPressure':
            queryset = queryset.exclude(systolic_pressure__isnull=True).exclude(diastolic_pressure__isnull=True)
        elif record_type == 'heartRate':
            queryset = queryset.exclude(heart_rate__isnull=True)
        elif record_type == 'bloodSugar':
            queryset = queryset.exclude(blood_sugar__isnull=True)
            
        return queryset
    
    def _get_weight_statistics(self, queryset):
        """获取体重统计数据"""
        # 使用单个聚合查询获取统计数据
        stats = queryset.aggregate(
            avg_value=Avg('weight'),
            max_value=Max('weight'),
            min_value=Min('weight'),
            count=Count('id')
        )
        
        # 获取趋势数据
        trend_data = list(queryset
            .annotate(date=TruncDate('record_time'))
            .values('date')
            .annotate(avg_value=Avg('weight'))
            .order_by('date')
        )
        
        # 格式化数据
        data = []
        for item in trend_data:
            if item['date'] and item['avg_value']:
                data.append({
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'value': round(float(item['avg_value']), 2)
                })
        
        return {
            'average': round(float(stats['avg_value'] or 0), 2),
            'max': round(float(stats['max_value'] or 0), 2),
            'min': round(float(stats['min_value'] or 0), 2),
            'count': stats['count'] or 0,
            'data': data
        }
    
    def _get_blood_pressure_statistics(self, queryset):
        """获取血压统计数据"""
        # 使用单个聚合查询获取统计数据
        stats = queryset.aggregate(
            avg_systolic=Avg('systolic_pressure'),
            max_systolic=Max('systolic_pressure'),
            min_systolic=Min('systolic_pressure'),
            avg_diastolic=Avg('diastolic_pressure'),
            max_diastolic=Max('diastolic_pressure'),
            min_diastolic=Min('diastolic_pressure'),
            count=Count('id')
        )
        
        # 获取趋势数据
        trend_data = list(queryset
            .annotate(date=TruncDate('record_time'))
            .values('date')
            .annotate(
                avg_systolic=Avg('systolic_pressure'),
                avg_diastolic=Avg('diastolic_pressure')
            )
            .order_by('date')
        )
        
        # 格式化数据
        data = []
        for item in trend_data:
            if item['date'] and item['avg_systolic'] and item['avg_diastolic']:
                data.append({
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'systolic': round(float(item['avg_systolic']), 0),
                    'diastolic': round(float(item['avg_diastolic']), 0)
                })
        
        # 计算平均值
        avg_systolic = round(float(stats['avg_systolic'] or 0), 0)
        avg_diastolic = round(float(stats['avg_diastolic'] or 0), 0)
        
        return {
            'average': f"{avg_systolic}/{avg_diastolic}",
            'max': f"{round(float(stats['max_systolic'] or 0), 0)}/{round(float(stats['max_diastolic'] or 0), 0)}",
            'min': f"{round(float(stats['min_systolic'] or 0), 0)}/{round(float(stats['min_diastolic'] or 0), 0)}",
            'count': stats['count'] or 0,
            'data': data
        }
    
    def _get_heart_rate_statistics(self, queryset):
        """获取心率统计数据"""
        # 使用聚合查询获取统计数据
        stats = queryset.aggregate(
            avg_value=Avg('heart_rate'),
            max_value=Max('heart_rate'),
            min_value=Min('heart_rate'),
            count=Count('id')
        )
        
        # 获取趋势数据
        trend_data = list(queryset
            .annotate(date=TruncDate('record_time'))
            .values('date')
            .annotate(
                avg_value=Avg('heart_rate')
            )
            .order_by('date')
        )
        
        # 格式化数据
        data = []
        for item in trend_data:
            if item['date'] and item['avg_value']:
                data.append({
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'value': round(float(item['avg_value']), 0)  # 心率取整数
                })
        
        # 计算平均值
        avg_value = round(float(stats['avg_value'] or 0), 0)
        max_value = round(float(stats['max_value'] or 0), 0)
        min_value = round(float(stats['min_value'] or 0), 0)
        
        return {
            'average': str(avg_value),
            'max': str(max_value),
            'min': str(min_value),
            'count': stats['count'] or 0,
            'data': data
        }
    
    def _get_blood_sugar_statistics(self, queryset):
        """获取血糖统计数据"""
        # 使用聚合查询获取统计数据
        stats = queryset.aggregate(
            avg_value=Avg('blood_sugar'),
            max_value=Max('blood_sugar'),
            min_value=Min('blood_sugar'),
            count=Count('id')
        )
        
        # 获取趋势数据
        trend_data = list(queryset
            .annotate(date=TruncDate('record_time'))
            .values('date')
            .annotate(
                avg_value=Avg('blood_sugar')
            )
            .order_by('date')
        )
        
        # 格式化数据
        data = []
        for item in trend_data:
            if item['date'] and item['avg_value']:
                data.append({
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'value': round(float(item['avg_value']), 1)  # 血糖保留一位小数
                })
        
        # 计算平均值
        avg_value = round(float(stats['avg_value'] or 0), 1)
        max_value = round(float(stats['max_value'] or 0), 1)
        min_value = round(float(stats['min_value'] or 0), 1)
        
        return {
            'average': str(avg_value),
            'max': str(max_value),
            'min': str(min_value),
            'count': stats['count'] or 0,
            'data': data
        }

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取健康记录统计数据"""
        # 获取统计类型和周期参数
        record_type = request.query_params.get('type', 'weight')
        period = request.query_params.get('period', 'week')
        
        try:
            # 获取过滤后的查询集
            queryset = self._get_filtered_queryset(period, record_type)
            
            # 根据记录类型选择相应的处理函数
            if record_type == 'weight':
                result = self._get_weight_statistics(queryset)
            elif record_type == 'bloodPressure':
                result = self._get_blood_pressure_statistics(queryset)
            elif record_type == 'heartRate':
                result = self._get_heart_rate_statistics(queryset)
            elif record_type == 'bloodSugar':
                result = self._get_blood_sugar_statistics(queryset)
            else:
                return Response(
                    {"error": f"不支持的记录类型: {record_type}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(result)
        except Exception as e:
            # 统一异常处理
            print(f"健康统计发生错误: {str(e)}")
            return Response(
                {"error": "获取统计数据失败", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )