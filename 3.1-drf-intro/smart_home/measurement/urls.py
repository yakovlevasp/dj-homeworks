"""
URL-адреса приложения
"""
from django.urls import path

from .views import SensorView, SensorDetailView, MeasurementView


urlpatterns = [
    path('sensors/', SensorView.as_view(), name="sensors"),
    path('sensors/<pk>/', SensorDetailView.as_view(), name="sensors"),
    path('measurements/', MeasurementView.as_view(), name="measurements"),
]
