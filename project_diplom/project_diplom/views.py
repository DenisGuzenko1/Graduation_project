from django.shortcuts import render
from django.views.generic import ListView
from bicycle.models import Product
from .forms import Search

def about(request):
    return render(request, 'about.html')


def delivery(request):
    return render(request, 'delivery.html')

def project_search(request):
    result = []
    query = None
    if 'query' in request.GET:
        form = Search(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result = Product.objects.filter(name=f'{query}')

    else:
        form = Search()
    context = {'form': form, 'query': query, 'result': result}
    return render(request, 'search.html', context)
