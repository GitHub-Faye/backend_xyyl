from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('姓名', max_length=50, blank=True)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    age = models.IntegerField('年龄', null=True, blank=True)
    phone = models.CharField('手机号', max_length=11, blank=True)
    height = models.DecimalField('身高(cm)', max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField('体重(kg)', max_digits=5, decimal_places=2, null=True, blank=True)
    medical_history = models.TextField('既往病史', blank=True)
    allergies = models.TextField('过敏史', blank=True)
    
    # 微信小程序相关字段
    openid = models.CharField('微信OpenID', max_length=100, blank=True, null=True, unique=True)
    nickname = models.CharField('微信昵称', max_length=50, blank=True, null=True)
    avatar_url = models.URLField('头像URL', blank=True, null=True)
    city = models.CharField('城市', max_length=30, blank=True, null=True)
    province = models.CharField('省份', max_length=30, blank=True, null=True)
    country = models.CharField('国家', max_length=30, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f"{self.user.username}的资料"
