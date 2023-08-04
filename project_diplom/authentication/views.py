# Импортируем необходимые функции и классы из Django
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Импортируем модели Order и OrderItem из приложения order,
# а также формы LoginForm и RegisterForm из текущего приложения
from .forms import LoginForm, RegisterForm


# Представление для входа пользователя
def login_user(request):
    # Создаем контекст с формой LoginForm
    context = {'login_form': LoginForm()}

    # Если запрос методом POST
    if request.method == 'POST':
        # Создаем форму LoginForm на основе данных запроса
        login_form = LoginForm(request.POST)
        # Если форма допустима (валидна)
        if login_form.is_valid():
            # Получаем имя пользователя и пароль из формы
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # Аутентифицируем пользователя
            user = authenticate(username=username, password=password)
            # Если пользователь существует
            if user:
                # Авторизуем пользователя
                login(request, user)
                # Перенаправляем на первую страницу (first_page)
                return redirect('first_page')
            else:
                # Если пользователь не найден, обновляем контекст с ошибкой
                context = {
                    'login_form': login_form,
                    'attention': f'Пользователь с таким именем {username} и паролем не найден!'
                }
        else:
            # Если форма недопустима, обновляем контекст с ошибками
            context = {
                'login_form': login_form,
            }

    # Отправляем ответ с шаблоном 'login.html' и контекстом
    return render(request, 'login.html', context)


# Классовое представление для регистрации пользователя
class RegisterView(TemplateView):
    template_name = 'register.html'

    # Метод для обработки GET-запроса
    def get(self, request):
        # Создаем форму RegisterForm
        user_form = RegisterForm()
        # Создаем контекст с формой RegisterForm
        context = {'user_form': user_form}
        # Отправляем ответ с шаблоном 'register.html' и контекстом
        return render(request, 'register.html', context)

    # Метод для обработки POST-запроса
    def post(self, request):
        # Создаем форму RegisterForm на основе данных запроса
        user_form = RegisterForm(request.POST)
        # Если форма допустима (валидна)
        if user_form.is_valid():
            # Сохраняем пользователя в базу данных
            user = user_form.save()
            # Устанавливаем хэш пароля
            user.set_password(user.password)
            # Сохраняем изменения в пользователе
            user.save()
            # Авторизуем пользователя
            login(request, user)
            # Перенаправляем на первую страницу (first_page)
            return redirect('first_page')

        # Отправляем ответ с шаблоном 'register.html' и контекстом
        context = {'user_form': user_form}
        return render(request, 'register.html', context)


# Представление для выхода пользователя (разлогинивание)
def logout_user(request):
    # Выходим из аккаунта
    logout(request)
    # Перенаправляем на первую страницу (first_page)
    return redirect('first_page')
