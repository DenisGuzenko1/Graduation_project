from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from order.models import Order, OrderItem
from .forms import LoginForm, RegisterForm


# from .models import Profile

def login_user(request):
    context = {'login_form': LoginForm()}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('first_page')
            else:
                context = {
                    'login_form': login_form,
                    'attention': f'Пользователь с таким именем {username} и паролем не найден!'
                }
        else:
            context = {
                'login_form': login_form,
            }

    return render(request, 'login.html', context)


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get(self, request):
        user_form = RegisterForm()
        context = {'user_form': user_form}
        return render(request, 'register.html', context)

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('first_page')

        context = {'user_form': user_form}
        return render(request, 'register.html', context)


def logout_user(request):
    logout(request)
    return redirect('first_page')
