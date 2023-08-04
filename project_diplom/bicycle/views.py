from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from cart.forms import CartAddProductForm
from .models import Product, Category

@cache_page(60 * 15)
def product_index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    context = {
        'category': categories,
        'products': products,
    }
    return render(request, 'product_index.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product,
                                id=id,
                                available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_from': cart_product_form,
    }
    return render(request, 'product_detail.html', context)
