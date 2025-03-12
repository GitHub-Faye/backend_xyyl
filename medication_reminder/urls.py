from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationReminderViewSet

router = DefaultRouter()
router.register(r'reminders', MedicationReminderViewSet, basename='medication-reminder')

urlpatterns = [
    path('', include(router.urls)),
] 