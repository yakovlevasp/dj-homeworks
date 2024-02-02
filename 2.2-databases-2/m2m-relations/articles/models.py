"""
Модели таблиц
"""
from django.db import models


class Article(models.Model):
    """
    Модель таблицы для хранения статей
    """
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Модель таблицы разделов
    """
    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Scope(models.Model):
    """
    Модель таблицы связи статей и разделов
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной')
