from django.contrib import admin
from .models import MedicationReminder

@admin.register(MedicationReminder)
class MedicationReminderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'frequency', 'times', 'is_active', 'created_at')
    list_filter = ('frequency', 'is_active')
    search_fields = ('name', 'user__username', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'start_date')
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'name', 'description', 'is_active')
        }),
        ('服药周期', {
            'fields': ('frequency', 'weekdays', 'month_days', 'custom_interval')
        }),
        ('服药时间', {
            'fields': ('times', 'end_date')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at', 'start_date'),
            'classes': ('collapse',)
        }),
    )
