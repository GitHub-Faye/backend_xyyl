from django.contrib import admin
from .models import HealthRecord

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'systolic_pressure', 'diastolic_pressure', 
                   'heart_rate', 'record_time', 'created_at')
    list_filter = ('user', 'record_time')
    search_fields = ('user__username',)
    date_hierarchy = 'record_time'
