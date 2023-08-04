from decimal import Decimal  # Импорт класса Decimal из модуля decimal

from django.conf import settings  # Импорт настроек Django

from bicycle import models  # Импорт моделей приложения "bicycle"


class Cart:
    """
    Класс для работы с корзиной товаров в интернет-магазине.
    """

    def __init__(self, request):
        """
        Инициализируем корзину, получая данные из сессии или создавая новую корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество, если товар уже есть в корзине.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()  # Сохраняем корзину в сессии

    def save(self):
        """
        Сохраняем корзину в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Удаляем товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  # Сохраняем корзину после удаления товара

    def __iter__(self):
        """
        Итератор, который возвращает товары в корзине и их информацию.
        """
        bicycle_ids = self.cart.keys()
        bicycles = models.Product.objects.filter(id__in=bicycle_ids)
        for bicycle in bicycles:
            self.cart[str(bicycle.id)]['product'] = bicycle

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])  # Преобразуем цену в Decimal для точности вычислений
            item['total_price'] = item['price'] * item['quantity']  # Вычисляем общую стоимость товара
            yield item  # Возвращаем информацию о товаре в корзине

    def __len__(self):
        """
        Возвращает общее количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Возвращает общую стоимость всех товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Очищает корзину, удаляя все товары из сессии.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True  # Устанавливаем флаг модификации сессии для сохранения изменений
