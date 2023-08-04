from django.shortcuts import render  # Импорт функции render из модуля django.shortcuts

from bicycle.models import Product  # Импорт модели Product из приложения bicycle
from .forms import Search  # Импорт формы Search из текущего пакета (текущего приложения)


def about(request):
    """
    Представление для страницы "about".
    Возвращает шаблон "about.html" при обращении к данному URL.
    """
    return render(request, 'about.html')


def delivery(request):
    """
    Представление для страницы доставки.
    Возвращает шаблон "delivery.html" при обращении к данному URL.
    """
    return render(request, 'delivery.html')
