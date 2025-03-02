# Generated by Django 5.1.6 on 2025-03-02 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_userprofile_allergies_userprofile_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_url',
            field=models.URLField(blank=True, null=True, verbose_name='头像URL'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='国家'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='微信昵称'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='openid',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='微信OpenID'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='province',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='省份'),
        ),
    ]
