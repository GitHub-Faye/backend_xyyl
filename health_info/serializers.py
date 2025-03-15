from rest_framework import serializers
from .models import HealthRecord

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ['id', 'weight', 'systolic_pressure', 'diastolic_pressure', 
                 'heart_rate', 'blood_sugar', 'record_time', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """
        创建健康记录，支持单条和批量创建
        
        如果 validated_data 中已包含 user 字段（批量创建时），则直接使用
        否则从请求上下文中获取用户（单条创建时）
        """
        # 如果 validated_data 中没有 user 字段，则从请求上下文中获取
        if 'user' not in validated_data and 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data) 