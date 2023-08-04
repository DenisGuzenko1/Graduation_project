from django.db import models


class Category(models.Model):
    # Модель "Category" - категория продукта.
    name = models.CharField(max_length=255, blank=True, null=True, default=None)

    # Поле "name" типа "CharField" для хранения имени категории.

    def __str__(self):
        # Метод "__str__" возвращает строковое представление объекта модели.
        return self.name


class Product(models.Model):
    # Модель "Product" - продукт.
    article = models.CharField(max_length=10, blank=True, null=True, default=None)
    # Поле "article" типа "CharField" для хранения артикула продукта.
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    # Поле "name" типа "CharField" для хранения имени продукта.
    description = models.TextField(blank=True, null=True, default=None)
    # Поле "description" типа "TextField" для хранения описания продукта.
    stock = models.PositiveIntegerField()
    # Поле "stock" типа "PositiveIntegerField" для хранения количества продукта на складе.
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # Поле "price" типа "DecimalField" для хранения цены продукта.
    image = models.ImageField(upload_to='img/', blank=True, null=True, default=None)
    # Поле "image" типа "ImageField" для хранения изображения продукта.
    available = models.BooleanField(default=True)
    # Поле "available" типа "BooleanField" для хранения информации о доступности продукта.
    cat = models.ForeignKey('Category', models.CASCADE, blank=True, null=True, default=None)
    # Поле "cat" типа "ForeignKey" для связи продукта с категорией. Каскадное удаление связанных объектов.
    created = models.DateTimeField(auto_now_add=True)
    # Поле "created" типа "DateTimeField" для хранения даты и времени создания записи о продукте.
    # Автоматически заполняется при создании.
    updated = models.DateTimeField(auto_now=True)

    # Поле "updated" типа "DateTimeField" для хранения даты и времени последнего обновления записи о продукте.
    # Автоматически обновляется при сохранении объекта.

    def __str__(self):
        # Метод "__str__" возвращает строковое представление объекта модели.
        return self.name
