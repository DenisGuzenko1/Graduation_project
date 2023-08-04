from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from cart.forms import CartAddProductForm
from .models import Product, Category

@cache_page(60 * 15)
def product_index(request):
    """
    Представление для отображения списка продуктов (индексной страницы).

    Основные действия:
    1. Получает все категории товаров из базы данных.
    2. Получает все доступные продукты из базы данных.
    3. Создает контекст с данными о категориях и продуктах.
    4. Возвращает ответ с отображением шаблона "product_index.html" и контекстом.
    """
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'product_index.html', context)


def product_detail(request, id):
    """
    Представление для отображения деталей конкретного продукта.

    Основные действия:
    1. Получает продукт с заданным id из базы данных.
    2. Если продукт не найден или недоступен (available=False), вернет ошибку 404.
    3. Инициализирует форму CartAddProductForm для добавления продукта в корзину.
    4. Создает контекст с данными о продукте и формой.
    5. Возвращает ответ с отображением шаблона "product_detail.html" и контекстом.
    """
    product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'product_detail.html', context)
