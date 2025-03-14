# Generated by Django 5.1.6 on 2025-03-01 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='allergies',
            field=models.TextField(blank=True, verbose_name='过敏史'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='出生日期'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='medical_history',
            field=models.TextField(blank=True, verbose_name='既往病史'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='体重(kg)'),
        ),
    ]
