"""
View-функции
"""
from django.shortcuts import render
from django.db.models import Prefetch

from articles.models import Article, Scope


def articles_list(request):
    """
    View-функция страницы новостей
    """
    template = 'articles/news.html'
    context = {
        'object_list': Article.objects.prefetch_related(
            Prefetch('scopes', queryset=Scope.objects.order_by('-is_main', 'tag__name'))
        )
    }
    return render(request, template, context)
