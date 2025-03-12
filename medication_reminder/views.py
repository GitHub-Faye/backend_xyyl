from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import MedicationReminder
from .serializers import MedicationReminderSerializer

# Create your views here.

class MedicationReminderViewSet(viewsets.ModelViewSet):
    """药物提醒视图集"""
    serializer_class = MedicationReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """只返回当前用户的药物提醒"""
        return MedicationReminder.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """创建时自动关联当前用户"""
        serializer.save(user=self.request.user)
