from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog),
    path("login", views.login),
    path("cart", views.cart),
    path("orders", views.orders),
    path("product/<int:id>", views.product),
    path("profile", views.profile)
]
