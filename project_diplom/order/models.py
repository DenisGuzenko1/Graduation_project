from django.db import models

from bicycle.models import Product


# Определяем модель для заказов.
class Order(models.Model):
    # Имя заказчика (строка, максимум 50 символов).
    first_name = models.CharField(max_length=50)
    # Фамилия заказчика (строка, максимум 50 символов).
    last_name = models.CharField(max_length=50)
    # Email заказчика.
    email = models.EmailField()
    # Адрес заказа (строка, максимум 250 символов).
    address = models.CharField(max_length=250)
    # Почтовый индекс заказа (строка, максимум 20 символов).
    postal_code = models.CharField(max_length=20)
    # Город заказа (строка, максимум 100 символов).
    city = models.CharField(max_length=100)
    # Дата и время создания заказа (автоматически устанавливается при создании).
    created = models.DateTimeField(auto_now_add=True)
    # Дата и время последнего обновления заказа (автоматически обновляется при изменениях).
    updated = models.DateTimeField(auto_now=True)
    # Признак оплаты заказа (по умолчанию False, т.е. неоплачен).
    paid = models.BooleanField(default=False)

    # Мета-класс для определения метаданных модели.
    class Meta:
        # Сортировка заказов по умолчанию - в обратном порядке по дате создания.
        ordering = ('-created',)
        # Наименование модели в единственном числе.
        verbose_name = 'Заказ'
        # Наименование модели во множественном числе.
        verbose_name_plural = 'Заказы'

    # Метод, возвращающий строковое представление заказа.
    def __str__(self):
        return 'Order {}'.format(self.id)

    # Метод для вычисления общей стоимости заказа.
    def get_total_cost(self):
        # Суммируем стоимость каждого элемента заказа, умноженную на его количество.
        return sum(item.get_cost() for item in self.items.all())


# Определяем модель для элементов заказа.
class OrderItem(models.Model):
    # Ссылка на заказ (связь "многие к одному" с моделью Order).
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Ссылка на продукт (связь "многие к одному" с моделью Product).
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    # Цена элемента заказа (десятичное число с 10 знаками и 2 знаками после запятой).
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Количество продуктов в заказе (целое положительное число, по умолчанию 1).
    quantity = models.PositiveIntegerField(default=1)

    # Метод, возвращающий строковое представление элемента заказа.
    def __str__(self):
        return '{}'.format(self.id)

    # Метод для вычисления стоимости элемента заказа.
    def get_cost(self):
        # Вычисляем общую стоимость элемента (цена * количество).
        return self.price * self.quantity
