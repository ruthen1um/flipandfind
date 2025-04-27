from django.urls import path, include

urlpatterns = [
    path('', include('store.urls.buyer')),
    path('seller', include('store.urls.seller')),
]
