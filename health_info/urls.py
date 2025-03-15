from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthRecordViewSet

router = DefaultRouter()
router.register(r'health-records', HealthRecordViewSet, basename='health-record')

urlpatterns = [
    # 只包含路由器生成的URLs，动作路由会自动注册为 /health-records/batch/
    path('', include(router.urls)),
] 