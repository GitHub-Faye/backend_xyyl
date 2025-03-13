from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import MedicationReminder
from .serializers import MedicationReminderSerializer
import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"用户 {self.request.user.username} 正在创建新的药物提醒")
        serializer.save(user=self.request.user)
        logger.info("药物提醒创建成功")

    def update(self, request, *args, **kwargs):
        """更新药物提醒"""
        logger.info(f"用户 {request.user.username} 正在更新药物提醒 ID: {kwargs.get('pk')}")
        logger.debug(f"更新数据: {request.data}")
        
        try:
            response = super().update(request, *args, **kwargs)
            if response.status_code == 200:
                logger.info("药物提醒更新成功")
            else:
                logger.warning(f"药物提醒更新失败，状态码: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"更新药物提醒时发生错误: {str(e)}")
            raise

    def destroy(self, request, *args, **kwargs):
        """删除药物提醒"""
        logger.info(f"用户 {request.user.username} 正在删除药物提醒 ID: {kwargs.get('pk')}")
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info("药物提醒删除成功")
            return response
        except Exception as e:
            logger.error(f"删除药物提醒时发生错误: {str(e)}")
            raise
