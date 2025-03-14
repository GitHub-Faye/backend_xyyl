# Generated by Django 5.1.6 on 2025-02-28 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='姓名')),
                ('gender', models.CharField(blank=True, choices=[('M', '男'), ('F', '女'), ('O', '其他')], max_length=1, verbose_name='性别')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('phone', models.CharField(blank=True, max_length=11, verbose_name='手机号')),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='身高(cm)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户资料',
                'verbose_name_plural': '用户资料',
            },
        ),
    ]
