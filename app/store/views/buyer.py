from django.shortcuts import render
from django.http import HttpRequest

from store.models.product import Product


def catalog(request: HttpRequest):
    featured_products = Product.objects.all()
    recommended_products = Product.objects.all()
    context = {
        'featured_products': featured_products,
        'recommended_product': recommended_products,
    }
    return render(request, "buyer/catalog.html", context=context)


def product(request: HttpRequest, id: int):
    return render(request, "buyer/product.html")


def login(request: HttpRequest):
    return render(request, "buyer/login.html")


def cart(request: HttpRequest):
    return render(request, "buyer/cart.html")


def orders(request: HttpRequest):
    return render(request, "buyer/orders.html")


def profile(request: HttpRequest):
    return render(request, "buyer/profile.html")
