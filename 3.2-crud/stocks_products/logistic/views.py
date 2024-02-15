"""
Представления
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    """
    ViewSet для продуктов
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # параметры фильтрации
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    pagination_class = PageNumberPagination


class StockViewSet(ModelViewSet):
    """
    ViewSet для складов
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # параметры фильтрации
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
    pagination_class = PageNumberPagination
