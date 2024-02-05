"""
Cериализаторы
"""
from rest_framework import serializers

from .models import Project, Measurement


class ProjectSerializer(serializers.ModelSerializer):
    """
    Cериализатор соответствующий модели объекта
    """
    class Meta:
        model = Project
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Cериализатор соответствующий модели измерения
    """
    class Meta:
        model = Measurement
        fields = '__all__'
