"""
View-функции
"""
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max, Min

from books.models import Book


def books_view(request):
    """
    View-функция главной страницы
    """
    template = 'books/books_list.html'
    context = {}
    return render(request, template, context)


def books_catalog(request):
    """
    View-функция страницы каталога книг
    """
    template = 'books/catalog.html'
    context = {
        'books': Book.objects.order_by('pub_date')
    }
    return render(request, template, context)


def books_by_date(request, pub_date_str):
    """
    View-функция списка книг за дату
    """
    try:
        pub_date = datetime.datetime.strptime(pub_date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse(
            "Некорректная дата публикации", status=400, reason="Incorrect data"
        )

    next_pub = Book.objects.filter(pub_date__gt=pub_date).aggregate(Min('pub_date'))
    prev_pub = Book.objects.filter(pub_date__lt=pub_date).aggregate(Max('pub_date'))
    context = {
        'books': Book.objects.filter(pub_date=pub_date),
        'next_date': next_pub.get('pub_date__min'),
        'prev_date': prev_pub.get('pub_date__max')
    }
    return render(request, 'books/catalog.html', context)
