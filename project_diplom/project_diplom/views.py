from django.shortcuts import render


def about(request):
    return render(request, 'about.html')


def delivery(request):
    return render(request, 'delivery.html')
