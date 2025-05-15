"""
URL configuration for flipandfind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import buyer
from django.views.defaults import page_not_found


def custom_404_handler(request, exception):
    path = request.path

    if not path.startswith('/seller/'):
        return buyer.page_not_found(request, exception)

    return page_not_found(request, exception)


handler404 = custom_404_handler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('api/catalog/', buyer.api_catalog),
    path('api/cart/add/<int:product_id>/', buyer.api_add_to_cart),
    path('api/cart/remove/<int:product_id>/', buyer.api_remove_from_cart),
    path('api/cart/update/<int:product_id>/', buyer.api_update_quantity),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
