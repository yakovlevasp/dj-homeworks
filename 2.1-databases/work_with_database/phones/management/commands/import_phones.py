"""
Модуль с пользовательскими командами
"""
import ast
import csv
import datetime


from django.utils import text
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    """
    Класс команды добавления телефонов в бд
    """
    def handle(self, *args, **options):
        """
        Перенос данных из csv-файла в модель Phone
        """
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            Phone.objects.create(
                name=phone['name'],
                price=float(phone['price']),
                image=phone['image'],
                release_date=datetime.datetime.strptime(phone['release_date'], '%Y-%m-%d').date(),
                lte_exists=ast.literal_eval(phone['lte_exists']),
                slug=text.slugify(phone['name'])
            )
