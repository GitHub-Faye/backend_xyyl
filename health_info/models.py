from django.db import models
from django.contrib.auth.models import User

class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='体重(kg)')
    systolic_pressure = models.IntegerField(verbose_name='收缩压(mmHg)')
    diastolic_pressure = models.IntegerField(verbose_name='舒张压(mmHg)')
    heart_rate = models.IntegerField(verbose_name='心率(次/分钟)')
    blood_sugar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='血糖(mmol/L)')
    record_time = models.DateTimeField(verbose_name='记录时间')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_time']
        verbose_name = '健康记录'
        verbose_name_plural = '健康记录'
        # 添加索引以提高查询性能
        indexes = [
            models.Index(fields=['user', 'record_time']),  # 复合索引，提高按用户和时间过滤的查询
            models.Index(fields=['record_time']),  # 单独的时间索引
            models.Index(fields=['user', 'weight']),  # 用户体重查询索引
            models.Index(fields=['user', 'systolic_pressure', 'diastolic_pressure']),  # 用户血压查询索引
            models.Index(fields=['user', 'heart_rate']),  # 用户心率查询索引
            models.Index(fields=['user', 'blood_sugar']),  # 用户血糖查询索引
        ]

    def __str__(self):
        return f"{self.user.username} - {self.record_time}"
