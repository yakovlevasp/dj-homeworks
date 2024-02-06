"""
Модели
"""
from django.db import models


class Sensor(models.Model):
    """
    Модель датчика
    """
    name = models.TextField()
    description = models.TextField()


class Measurement(models.Model):
    """
    Модель измерения
    """
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='measurement/img', null=True)
