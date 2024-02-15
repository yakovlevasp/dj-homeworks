"""
Сериализаторы
"""
from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продукта
    """
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для позиции продукта на складе
    """
    class Meta:
        model = StockProduct
        fields = ['id', 'quantity', 'price', 'product']


class StockSerializer(serializers.ModelSerializer):
    """
    Сериализатор для склада
    """
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    @staticmethod
    def _update_related_products(stock, positions):
        """
        Заполнение связанной таблицы StockProduct
        """
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)

    def create(self, validated_data):
        """
        Создание склада и заполнение связанных продуктов
        """
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        # обновляем связанную таблицу StockProduct
        # с помощью списка positions
        self._update_related_products(stock, positions)

        return stock

    def update(self, instance, validated_data):
        """
        Обновление склада и заполнение связанных продуктов
        """
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # обновляем связанную таблицу StockProduct
        # с помощью списка positions
        self._update_related_products(stock, positions)

        return stock
