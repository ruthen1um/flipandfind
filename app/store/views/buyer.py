from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse

import random
from store.models.product import Product

PRODUCTS_PER_PAGE = 5
MAX_FEATURED_PRODUCTS = 4
MAX_SIMILAR_PRODUCTS = 5


def catalog(request: HttpRequest):
    all_products = Product.objects.all()

    featured_products = (
        random.sample(
            list(all_products),
            min(len(all_products), MAX_FEATURED_PRODUCTS))
        if all_products else []
    )

    return render(request, 'buyer/catalog.html', {
        'featured_products': featured_products,
    })


def catalog_api(request):
    page = request.GET.get('page')

    if not page or not page.isdigit():
        return JsonResponse(
            {'error': 'Missing or invalid "page" parameter'}, status=400)

    product_list = Product.objects.all()
    paginator = Paginator(product_list, PRODUCTS_PER_PAGE)

    try:
        products_page = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'products': []})

    # Serialize products manually (or use serializers if preferred)
    products_data = [
        {
            'url': reverse('store_buyer:product', args=[product.id]),
            'primary_photo_url': product.primary_photo.url
            if product.primary_photo else None,
            'name': product.name,
            'seller_username': product.seller.username,
            'price': str(product.price),
            'average_rating': str(product.average_rating),
            'reviews_count': product.reviews_count,
        }
        for product in products_page.object_list
    ]

    return JsonResponse({
        'products': products_data,
        'has_next': products_page.has_next(),
    })


def product(request: HttpRequest, id: int):
    product = get_object_or_404(Product, pk=id)

    similar_products = (
        Product.objects
        .filter(category=product.category)
        .exclude(pk=product.pk)[:MAX_SIMILAR_PRODUCTS]
    )

    return render(request, "buyer/product.html", {
        'product': product,
        'similar_products': similar_products
    })


def login(request: HttpRequest):
    return render(request, "buyer/login.html")


def cart(request: HttpRequest):
    return render(request, "buyer/cart.html")


def orders(request: HttpRequest):
    return render(request, "buyer/orders.html")


def profile(request: HttpRequest):
    return render(request, "buyer/profile.html")


def page_not_found(request: HttpRequest, exception):
    return render(request, "buyer/404.html", status=404)
