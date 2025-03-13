from rest_framework import serializers
from .models import MedicationReminder
import logging

logger = logging.getLogger(__name__)

class MedicationReminderSerializer(serializers.ModelSerializer):
    """药物提醒序列化器"""
    
    class Meta:
        model = MedicationReminder
        fields = [
            'id', 'name', 'description', 'frequency', 'weekdays',
            'month_days', 'custom_interval', 'times',
            'start_date', 'end_date', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'start_date']
    
    def validate(self, data):
        """根据频率类型验证相关字段"""
        logger.info("开始验证药物提醒数据")
        logger.debug(f"验证数据: {data}")
        
        # 获取当前请求方法
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            logger.info("检测到PATCH请求，仅验证提供的字段")
            # 如果是PATCH请求，只验证提供的字段
            if 'frequency' in data:
                frequency = data.get('frequency')
                
                if frequency == 'weekly' and 'weekdays' in data and not data.get('weekdays'):
                    logger.warning("每周服药缺少星期几信息")
                    raise serializers.ValidationError("每周服药需要指定星期几")
                
                if frequency == 'monthly' and 'month_days' in data and not data.get('month_days'):
                    logger.warning("每月服药缺少日期信息")
                    raise serializers.ValidationError("每月服药需要指定具体日期")
                
                if frequency == 'custom' and 'custom_interval' in data and not data.get('custom_interval'):
                    logger.warning("自定义服药周期缺少间隔天数")
                    raise serializers.ValidationError("自定义服药周期需要指定间隔天数")
            
            if 'times' in data and not data.get('times'):
                logger.warning("提供了times字段但为空")
                raise serializers.ValidationError("服药时间不能为空")
            
            logger.info("PATCH请求数据验证通过")
            return data
            
        # 对于其他请求方法（POST、PUT），保持原有的完整验证
        frequency = data.get('frequency')
        
        if frequency == 'weekly' and not data.get('weekdays'):
            logger.warning("每周服药缺少星期几信息")
            raise serializers.ValidationError("每周服药需要指定星期几")
        
        if frequency == 'monthly' and not data.get('month_days'):
            logger.warning("每月服药缺少日期信息")
            raise serializers.ValidationError("每月服药需要指定具体日期")
        
        if frequency == 'custom' and not data.get('custom_interval'):
            logger.warning("自定义服药周期缺少间隔天数")
            raise serializers.ValidationError("自定义服药周期需要指定间隔天数")
        
        if not data.get('times'):
            logger.warning("缺少服药时间")
            raise serializers.ValidationError("需要指定服药时间")
        else:
            logger.debug(f"服药时间: {data.get('times')}")
        
        logger.info("数据验证通过")
        return data 