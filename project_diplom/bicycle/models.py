from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField(max_length=10, blank=True, null=True, default=None)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='img/', blank=True, null=True, default=None)
    available = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', models.CASCADE, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
