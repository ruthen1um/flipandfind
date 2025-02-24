from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("login", views.login, name="login"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders"),
    path("product/<int:id>", views.product, name="product"),
    path("profile", views.profile, name="profile")
]
