from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage

import random
from store.models.product import Product


def catalog(request: HttpRequest):
    all_products = Product.objects.all()

    featured_products = random.sample(
        list(all_products), min(len(all_products), 6)) if all_products else []

    return render(request, 'buyer/catalog.html', {
        'featured_products': featured_products,
    })


def catalog_api(request):
    page = request.GET.get('page')
    page_size = 6

    if not page or not page.isdigit():
        return HttpResponseBadRequest("Missing or invalid 'page' parameter")

    product_list = Product.objects.all()
    paginator = Paginator(product_list, page_size)

    try:
        products_page = paginator.page(page)
    except EmptyPage:
        return HttpResponse('')

    html = ''
    for product in products_page.object_list:
        html += render(
            request,
            'buyer/_product_card.html',
            {'product': product}
        ).content.decode('utf-8')

    return HttpResponse(html)


def product(request: HttpRequest, id: int):
    product = get_object_or_404(Product, pk=id)

    similar_products = (
        Product.objects
        .filter(category=product.category)
        .exclude(pk=product.pk)[:6]
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
