"""
View-функции
"""
from django.shortcuts import render, redirect

from phones.models import Phone


SORT_MAP = {
    'name': 'name',
    'min_price': 'price',
    'max_price': '-price',
}


def index(request):
    """
    View-функция главной страницы. Перенаправление на каталог
    """
    return redirect('catalog')


def show_catalog(request):
    """
    View-функция страницы каталога телефонов
    """
    template = 'catalog.html'

    phones = Phone.objects.all()
    sort = request.GET.get('sort')
    if sort:
        phones = phones.order_by(SORT_MAP[sort])

    return render(request, template, {'phones': phones})


def show_product(request, slug):
    """
    View-функция страницы телефона
    """
    template = 'product.html'
    context = {
        'phone': Phone.objects.get(slug=slug)
    }
    return render(request, template, context)
