from django.urls import path

from store.views import seller

app_name = "store_seller"

urlpatterns = [
    path("start", seller.start, name="start"),
    path("login", seller.login, name="login"),
    path("dashboard", seller.dashboard, name="dashboard"),
    path("reviews", seller.reviews, name="reviews"),
]
