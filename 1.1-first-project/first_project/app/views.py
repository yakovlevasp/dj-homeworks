"""
Django view functions
"""
import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    """
    View-функция главной страницы
    """
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    """
    View-функция страницы, показывающей текущую дату и время
    """
    # обратите внимание – здесь HTML шаблона нет,
    # возвращается просто текст
    current_time = datetime.datetime.now()
    msg = f'Текущее время: {current_time.strftime("%d.%m.%Y %H:%M:%S")}'
    return HttpResponse(msg)


def workdir_view(request):
    """
    View-функция страницы с содержимым рабочей директории
    """
    dir_content = '</p><p>'.join(os.listdir())
    return HttpResponse(f'<h1>Cписок файлов:</h1><p>{dir_content}</p>')
