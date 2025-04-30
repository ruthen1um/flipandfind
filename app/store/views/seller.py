from django.shortcuts import render
from django.http import HttpRequest


def start(request: HttpRequest):
    return render(request, "seller/start.html")


def login(request: HttpRequest):
    return render(request, "seller/login.html")


def dashboard(request: HttpRequest):
    return render(request, "seller/dashboard.html")


def reviews(request: HttpRequest):
    return render(request, "seller/reviews.html")
