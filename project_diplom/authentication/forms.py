from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    # Форма для входа пользователя
    username = forms.CharField()  # Поле для ввода имени пользователя
    password = forms.CharField(widget=forms.PasswordInput())  # Поле для ввода пароля с маскировкой

    def clean(self):
        # Переопределение метода clean для проверки данных формы
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            self.user = User.objects.get(username=username)  # Получение пользователя с указанным именем
        except User.DoesNotExist:
            # Если пользователь не найден, генерируем исключение
            raise forms.ValidationError(f'Пользователь с таким именем {username} не существует')

        if not self.user.check_password(password):
            # Проверяем правильность введенного пароля
            raise forms.ValidationError(f'Пароль этого пользователя {username} введен неверно!')


class RegisterForm(forms.ModelForm):
    # Форма для регистрации пользователя
    def __init__(self, *args, **kwargs):
        # Переопределение конструктора формы для установки обязательного поля email
        # и применения класса CSS к видимым полям
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-input'

    class Meta:
        model = User  # Используем модель User для создания формы
        fields = ('username', 'email', 'password')  # Определяем поля, которые будут отображаться в форме
        widgets = {
            'password': forms.PasswordInput()  # Поле для ввода пароля с маскировкой
        }


class ProfileForm(forms.ModelForm):
    # Форма для редактирования профиля пользователя
    class Meta:
        model = Profile  # Используем модель Profile для создания формы
        fields = '__all__'  # Определяем все поля модели, которые будут отображаться в форме

        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',  # Добавляем класс CSS для поля ввода
                'placeholder': 'Фамилия',  # Устанавливаем подсказку (placeholder) для поля ввода
                'title': 'Фамилия'  # Устанавливаем всплывающую подсказку (title) для поля ввода
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'title': 'Имя'
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество',
                'title': 'Отчество'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта',
                'title': 'Электронная почта',
            }),
            'phoneNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон',
                'title': 'Телефон'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес доставки',
                'title': 'Адрес доставки'
            })
        }
