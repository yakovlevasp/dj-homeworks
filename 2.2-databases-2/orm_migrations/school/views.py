"""
View-функции
"""
from django.shortcuts import render

from .models import Student


def students_list(request):
    """
    View-функция списка учеников
    """
    template = 'school/students_list.html'

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'
    context = {
        'object_list': Student.objects.order_by(ordering).prefetch_related('teacher')
    }
    return render(request, template, context)
