from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import LoginForm, RegisterForm, ProfileForm
from order.models import Order, OrderItem
from .models import Profile

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
                    'attention': f'The user with username {username} and password not found!'
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

def profile(request):
    context = {'profile_form': ProfileForm()}

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        profile = request.POST
        profile.patronymic = request.POST.get("patronymic")
        profile.phoneNumber = request.POST.get("phoneNumber")
        profile.address = request.POST.get("address")
        profile.first_name = request.POST.get("first_name")
        profile.last_name = request.POST.get("last_name")

        context = {'profile': profile}

    return render(request, 'profile.html', context)


class ProfilePage(TemplateView):
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        # try:
        # Определяем, какой раздел Личного кабинета открыть (он может прийти в строке url)
        chapter = 'profile'
        if 'data' in kwargs:
            chapter = kwargs['data']

        if request.user.is_authenticated:

            # Подготовка и работа с Профилем пользователя
            profile_data = Profile.objects.filter(user=request.user)
            profile = profile_data.get_user_data()

            if chapter == 'profile':

                if request.method == 'POST':
                    # Сохраняем данные пользователя не проверяя
                    profile = request.POST
                    profile_data.patronymic = request.POST.get("patronymic")
                    profile_data.phoneNumber = request.POST.get("phoneNumber")
                    profile_data.address = request.POST.get("address")
                    profile_data.save()
                    request.user.first_name = request.POST.get("first_name")
                    request.user.last_name = request.POST.get("last_name")
                    request.user.save()

        return render(request, self.template_name, locals())

def orders(request):
    my_orders = Order.objects.filter(first_name=request.user)
    orderitems = OrderItem.objects.all()
    context = {'my_orders': my_orders,
               'orderitems': orderitems}
    return render(request, 'orders.html', context)
