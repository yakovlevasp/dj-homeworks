"""
Модели админки
"""
from django.contrib import admin

from .models import Article, Tag, Scope
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ScopeInlineFormset(BaseInlineFormSet):
    """
    FormSet разделов
    """
    def clean(self):
        """
        Проверка разделов статьи.
        Проверяем, что для статьи выбран один основной раздел.
        А также, что раздел уникален в рамках статьи.
        """
        main_tag_exists = False
        tag_ids = set()
        for form in self.forms:
            scope = form.cleaned_data
            if not scope or self._should_delete_form(form):
                continue

            if scope.get('is_main') and main_tag_exists:
                form.add_error('is_main', "Основной раздел уже был выбран")
                raise ValidationError("Основной раздел должен быть только один")
            main_tag_exists = scope.get('is_main') or main_tag_exists

            if scope.get('tag'):
                if scope['tag'].pk in tag_ids:
                    form.add_error('tag', "Такой раздел уже добавлен.")
                else:
                    tag_ids.add(scope['tag'].pk)

        if not main_tag_exists:
            raise ValidationError("Не выбран основной раздел")

        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    """
    Встроенная модель выбора разделов
    """
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Модель для управления статьями
    """
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Модель для управления разделами
    """
    pass
