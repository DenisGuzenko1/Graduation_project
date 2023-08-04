# Импорт функций из модуля django.shortcuts
# render используется для генерации ответа на запрос с использованием шаблона
# redirect используется для перенаправления на другой URL
# get_object_or_404 используется для получения объекта из базы данных по заданному условию или возвращения 404 ошибки,
# если объект не найден
from django.shortcuts import render, redirect, get_object_or_404
# Импорт декоратора require_POST из модуля django.views.decorators.http
# require_POST исп. для обеспечения обработки только POST-запросов, все остальные методы будут вернуть ошибку 405
from django.views.decorators.http import require_POST

# Импорт моделей из приложения bicycle
import bicycle.models
# Импорт класса Cart из текущего модуля
from .cart import Cart
# Импорт формы CartAddProductForm из текущего модуля
from .forms import CartAddProductForm


# Декоратор require_POST обеспечивает, что данное представление будет обрабатывать только POST-запросы
@require_POST
def cart_add(request, id):
    # Создаем экземпляр класса Cart, передавая текущий запрос в качестве аргумента
    cart = Cart(request)
    # Получаем объект Product из базы данных с указанным id, если он существует. Если нет, вернется ошибка 404
    product = get_object_or_404(bicycle.models.Product, id=id)
    # Создаем форму CartAddProductForm, используя данные из POST-запроса
    form = CartAddProductForm(request.POST)
    # Проверяем, является ли форма валидной (все поля заполнены корректно)
    if form.is_valid():
        # Извлекаем очищенные данные из формы
        cd = form.cleaned_data
        # Вызываем метод add у объекта cart, чтобы добавить продукт в корзину с указанным количеством
        # и параметром обновления количества
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    # Перенаправляем пользователя на страницу корзины
    return redirect('cart_detail')


def cart_remove(request, id):
    # Создаем экземпляр класса Cart, передавая текущий запрос в качестве аргумента
    cart = Cart(request)
    # Получаем объект Product из базы данных с указанным id, если он существует. Если нет, вернется ошибка 404
    product = get_object_or_404(bicycle.models.Product, id=id)
    # Удаляем продукт из корзины, вызывая соответствующий метод у объекта cart
    cart.remove(product)
    # Перенаправляем пользователя на страницу корзины
    return redirect('cart_detail')


def cart_detail(request):
    # Создаем экземпляр класса Cart, передавая текущий запрос в качестве аргумента
    cart = Cart(request)
    # Отображаем шаблон 'detail.html', передавая в него объект cart через контекст
    return render(request, 'detail.html', {'cart': cart})
