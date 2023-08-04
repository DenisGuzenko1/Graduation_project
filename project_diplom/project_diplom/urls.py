"""
URL configuration for project_diplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from project_diplom import views
from .views import Search

from project_diplom import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('first_page.urls'), name='first_page'),
    path('bicycle/', include('bicycle.urls'), name='bicycle'),
    path('cart/', include('cart.urls'), name='cart'),
    path('auth/', include('authentication.urls'), name='auth'),
    path('order/', include('order.urls'), name='order'),
    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),
    path('search/', views.project_search, name='search'),
    path('payments/', include('payments.urls'), name='payments'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
