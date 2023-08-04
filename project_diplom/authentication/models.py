from django.conf import settings  # Импорт настроек Django
from django.contrib.auth import get_user_model  # Функция для получения модели пользователя
from django.core.validators import RegexValidator  # Импорт класса для валидации данных по регулярному выражению
from django.db import models  # Импорт модуля для работы с базой данных

User = get_user_model()  # Получение модели пользователя, используемой в проекте


# Модель "Profile" для хранения дополнительных данных пользователей
class Profile(models.Model):
    patronymic = models.CharField(max_length=64, blank=True, verbose_name=u'Отчество')  # Поле для отчества пользователя
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")  # Валидатор для номера телефона
    phoneNumber = models.CharField(validators=[phoneNumberRegex], blank=True, max_length=16,
                                   verbose_name=u'Телефон')  # Поле для номера телефона пользователя
    address = models.CharField(max_length=128, blank=True, verbose_name=u'Адрес доставки')  # Поле для адреса доставки
    cart = models.CharField(max_length=256, blank=True,
                            verbose_name=u'Корзина')  # Поле для хранения корзины (не используется?)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)  # Одно к одному с моделью пользователя

    class Meta:
        verbose_name = 'Профиль пользователя'  # Название для одиночного экземпляра модели
        verbose_name_plural = 'Профили пользователей'  # Название для множественных экземпляров модели

    # Метод для проверки, заполнены ли все данные пользователя в профиле
    # Возвращает True, если все поля заполнены, иначе - False
    def is_filled(self):
        user = self.user
        return bool(user.last_name and user.first_name and self.patronymic and self.phoneNumber and self.address)

    # Метод для получения словаря со всеми данными текущего пользователя из моделей User и Profile
    def get_user_data(self):
        return {
            'last_name': self.user.last_name,
            'first_name': self.user.first_name,
            'patronymic': self.patronymic,
            'email': self.user.email,
            'phoneNumber': self.phoneNumber,
            'address': self.address,
        }
