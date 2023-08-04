from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem


# Создаем представление для создания заказа
def order_create(request):
    # Получаем корзину текущего пользователя
    cart = Cart(request)

    if request.method == 'POST':
        # Если запрос методом POST, создаем форму заказа и передаем данные из запроса
        form = OrderCreateForm(request.POST)

        # Проверяем, что данные формы прошли валидацию
        if form.is_valid():
            # Если форма действительна, создаем объект заказа, но не сохраняем его в базе данных
            order = form.save()

            # Создаем объекты OrderItem для каждого элемента корзины и связываем их с заказом
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # После создания всех OrderItem, очищаем корзину
            cart.clear()

            # Отображаем страницу "created.html" с информацией о заказе
            return render(request, 'created.html', {'order': order})

    else:
        # Если запрос не методом POST, создаем пустую форму заказа
        form = OrderCreateForm()

    # Отображаем страницу "create.html" с данными о корзине и формой заказа
    return render(request, 'create.html', {'cart': cart, 'form': form})
