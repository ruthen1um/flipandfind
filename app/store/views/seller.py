from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpRequest
from store.models import User
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


def registration(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not password1 or not password2:
            return render(request, 'seller/registration.html', {
                'error': 'Все поля обязательны для заполнения'
            })

        if password1 != password2:
            return render(request, 'seller/registration.html', {
                'error': 'Пароли не совпадают'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'seller/registration.html', {
                'error': 'Пользователь с таким email уже существует'
            })

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1
            )
            user.role = User.Role.SELLER
            user.save()
        except Exception:
            return render(request, 'seller/registration.html', {
                'error': 'Ошибка при регистрации'
            })

        auth.login(request, user)
        return redirect('store_seller:dashboard')

    return render(request, 'seller/registration.html')


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('store_seller:login')


@login_required_seller
def dashboard(request: HttpRequest):
    return render(request, 'seller/dashboard.html')


@login_required_seller
def reviews(request: HttpRequest):
    return render(request, 'seller/reviews.html')
