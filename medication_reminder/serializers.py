from rest_framework import serializers
from .models import MedicationReminder

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
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """根据频率类型验证相关字段"""
        frequency = data.get('frequency')
        
        if frequency == 'weekly' and not data.get('weekdays'):
            raise serializers.ValidationError("每周服药需要指定星期几")
        
        if frequency == 'monthly' and not data.get('month_days'):
            raise serializers.ValidationError("每月服药需要指定具体日期")
        
        if frequency == 'custom' and not data.get('custom_interval'):
            raise serializers.ValidationError("自定义服药周期需要指定间隔天数")
        
        if not data.get('times'):
            raise serializers.ValidationError("需要指定服药时间")
        
        return data 