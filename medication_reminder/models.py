from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class MedicationReminder(models.Model):
    """药物提醒模型"""
    
    class FrequencyType(models.TextChoices):
        DAILY = 'daily', _('每天')
        WEEKLY = 'weekly', _('每周')
        MONTHLY = 'monthly', _('每月')
        CUSTOM = 'custom', _('自定义')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medication_reminders', verbose_name='用户')
    name = models.CharField('药物名称', max_length=100)
    description = models.TextField('用药说明', blank=True, null=True)
    
    # 服药周期相关
    frequency = models.CharField('服药频率', max_length=20, choices=FrequencyType.choices, default=FrequencyType.DAILY)
    
    # 如果是每周服药，存储星期几，例如 "1,3,5" 表示周一、周三、周五
    weekdays = models.CharField('每周服药日', max_length=20, blank=True, null=True, 
                              help_text='用逗号分隔的数字，1-7表示周一至周日')
    
    # 如果是每月服药，存储日期，例如 "1,15" 表示每月1日和15日
    month_days = models.CharField('每月服药日', max_length=100, blank=True, null=True,
                                help_text='用逗号分隔的数字，1-31表示每月具体日期')
    
    # 自定义间隔（以天为单位）
    custom_interval = models.PositiveIntegerField('自定义间隔天数', blank=True, null=True,
                                                help_text='以天为单位的自定义间隔')
    
    # 服药时间，格式为 "08:00,12:30,19:00"
    times = models.CharField('服药时间', max_length=100, 
                            help_text='用逗号分隔的时间字符串，格式为HH:MM')
    
    # 起止日期
    start_date = models.DateField('开始日期', auto_now_add=True)
    end_date = models.DateField('结束日期', blank=True, null=True)
    
    # 是否启用提醒
    is_active = models.BooleanField('是否启用', default=True)
    
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '药物提醒'
        verbose_name_plural = '药物提醒'
        
    def __str__(self):
        return f"{self.user.username} - {self.name}"
