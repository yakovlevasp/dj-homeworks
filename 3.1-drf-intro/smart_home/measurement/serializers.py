"""
Сериализаторы
"""
from rest_framework import serializers

from .models import Sensor, Measurement


class SensorSerializer(serializers.ModelSerializer):
    """
    Сериализатор соответствующий модели датчика
    """
    class Meta:
        model = Sensor
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Сериализатор соответствующий модели измерения
    """
    class Meta:
        model = Measurement
        fields = '__all__'


class SensorDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор с подробной информацией по датчику
    """
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
