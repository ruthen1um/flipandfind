from django.views.generic import RedirectView
from django.urls import path
from store.views import seller

app_name = "store_seller"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name='store_seller:dashboard', permanent=False)),
    path("start", seller.start, name="start"),
    path("login", seller.login, name="login"),
    path("registration", seller.registration, name="registration"),
    path("logout", seller.logout, name="logout"),
    path("dashboard", seller.dashboard, name="dashboard"),
    path("reviews", seller.reviews, name="reviews"),
]
