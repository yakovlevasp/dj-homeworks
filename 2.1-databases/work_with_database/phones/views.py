"""
View-функции
"""
from django.shortcuts import render, redirect

from phones.models import Phone


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
    sort_type = request.GET.get('sort')
    order = ()
    if sort_type == 'name':
        order = ('name',)
    elif sort_type == 'min_price':
        order = ('price',)
    elif sort_type == 'max_price':
        order = ('-price',)

    context = {
        'phones': Phone.objects.order_by(*order)
    }
    return render(request, template, context)


def show_product(request, slug):
    """
    View-функция страницы телефона
    """
    template = 'product.html'
    context = {
        'phone': Phone.objects.get(slug=slug)
    }
    return render(request, template, context)
