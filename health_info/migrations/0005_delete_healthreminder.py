# Generated by Django 5.1.6 on 2025-03-11 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_info', '0004_healthreminder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HealthReminder',
        ),
    ]
