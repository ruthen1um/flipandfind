from django.shortcuts import render
from django.http import HttpRequest


def catalog(request: HttpRequest):
    return render(request, "website/catalog.html")


def product(request: HttpRequest, id: int):
    return render(request, "website/product.html")


def login(request: HttpRequest):
    return render(request, "website/login.html")


def cart(request: HttpRequest):
    return render(request, "website/cart.html")


def orders(request: HttpRequest):
    return render(request, "website/orders.html")


def profile(request: HttpRequest):
    return render(request, "website/profile.html")
