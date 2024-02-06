"""
Представления
"""
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorView(ListCreateAPIView):
    """
    View для датчика
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementView(CreateAPIView):
    """
    View для измерения
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SensorDetailView(RetrieveUpdateAPIView):
    """
    View для подробной информации по датчику
    """
    queryset = Sensor.objects.all().prefetch_related('measurements')
    serializer_class = SensorDetailSerializer
