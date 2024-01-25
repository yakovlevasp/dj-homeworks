"""
Модуль моделей таблиц
"""
from django.db import models


class Phone(models.Model):
    """
    Модель таблицы телефонов
    """
    name = models.TextField(unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=1)
    image = models.TextField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.TextField(unique=True)
