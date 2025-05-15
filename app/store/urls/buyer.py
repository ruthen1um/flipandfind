from django.urls import path

from store.views import buyer

app_name = "store_buyer"

urlpatterns = [
    path("", buyer.catalog, name="catalog"),
    path("login", buyer.login, name="login"),
    path("logout", buyer.logout, name="logout"),
    path("cart", buyer.cart, name="cart"),
    path("orders", buyer.orders, name="orders"),
    path("product/<int:id>", buyer.product, name="product"),
    path("profile", buyer.profile, name="profile")
]
