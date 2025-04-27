from django.shortcuts import render
from django.http import HttpRequest


def catalog(request: HttpRequest):
    return render(request, "buyer/catalog.html")


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
