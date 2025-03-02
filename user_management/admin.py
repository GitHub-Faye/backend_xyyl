from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender', 'age', 'phone', 'height')
    search_fields = ('user__username', 'name', 'phone')
    list_filter = ('gender',)
