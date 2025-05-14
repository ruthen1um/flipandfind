from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.http import HttpRequest, HttpResponseRedirect
from store.models import User, Product, ProductPhoto
from functools import wraps


def login_required_seller(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('store_seller:login')
        if request.user.role != 'SELLER':
            return redirect('store_seller:login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def start(request: HttpRequest):
    return render(request, "seller/start.html")


def login(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)
        if user is not None and user.role == User.Role.SELLER:
            auth.login(request, user)
            return redirect('store_seller:dashboard')
        else:
            return render(request, 'seller/login.html', {
                'error': 'Неверный email или пароль'
            })

    return render(request, 'seller/login.html')


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('store_seller:login')


@login_required_seller
def dashboard(request: HttpRequest):
    return render(request, 'seller/dashboard.html')


@login_required_seller
def reviews(request: HttpRequest):
    return render(request, 'seller/reviews.html')
