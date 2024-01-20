"""
Django view functions
"""
import csv

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator


def index(request):
    """
    View-функция главной страницы. Перенаправление на список остановок
    """
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    """
    View-функция страницы со списком остановок
    """
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    context = {}
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as csvfile:
        paginator = Paginator(
            list(csv.DictReader(csvfile)),
            settings.BUS_STATION_PAGE_SIZE
        )
        context['page'] = paginator.get_page(request.GET.get('page', 1))
        context['bus_stations'] = context['page'].object_list
    return render(request, 'stations/index.html', context)
