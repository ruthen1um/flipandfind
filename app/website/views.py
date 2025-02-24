from django.shortcuts import render
from django.http import HttpRequest


def catalog(request: HttpRequest):
    return render(request, "catalog.html")


def product(request: HttpRequest, id: int):
    return render(request, "product.html")


def login(request: HttpRequest):
    return render(request, "login.html")


def cart(request: HttpRequest):
    return render(request, "cart.html")


def orders(request: HttpRequest):
    return render(request, "orders.html")


def profile(request: HttpRequest):
    return render(request, "profile.html")
