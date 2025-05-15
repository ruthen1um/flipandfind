from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from store.models import User
from functools import wraps

import random
from store.models.product import Product

PRODUCTS_PER_PAGE = 30
MAX_FEATURED_PRODUCTS = 4
MAX_SIMILAR_PRODUCTS = 5


def login_required_buyer(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('store_buyer:login')
        if request.user.role != 'BUYER':
            return redirect('store_buyer:login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def login(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)
        if user is not None and user.role == User.Role.BUYER:
            auth.login(request, user)
            return redirect('store_buyer:catalog')
        else:
            return render(request, 'buyer/login.html', {
                'error': 'Неверный email или пароль'
            })

    return render(request, 'buyer/login.html')


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('store_buyer:login')


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
    page = request.GET.get('page', '1')

    if not page.isdigit():
        return JsonResponse({'error': 'Invalid page number'}, status=400)

    all_product_ids = list(Product.objects.values_list('id', flat=True))

    session = request.session

    if 'current_shuffle' not in session:
        shuffled_ids = all_product_ids[:]
        random.shuffle(shuffled_ids)
        session['current_shuffle'] = shuffled_ids
        session.save()
    else:
        shuffled_ids = session['current_shuffle']

    paginator = Paginator(shuffled_ids, PRODUCTS_PER_PAGE)

    try:
        page_obj = paginator.page(int(page))
    except EmptyPage:
        return JsonResponse({'products': [], 'has_next': False})

    products_on_page = Product.objects.filter(id__in=page_obj.object_list).in_bulk()

    products_data = []
    for pid in page_obj.object_list:
        product = products_on_page[pid]
        products_data.append({
            'url': reverse('store_buyer:product', args=[product.id]),
            'primary_photo_url': product.primary_photo.url if product.primary_photo else None,
            'name': product.name,
            'seller_username': product.seller.username,
            'price': str(product.price),
            'average_rating': str(product.average_rating),
            'reviews_count': product.reviews_count,
        })

    return JsonResponse({
        'products': products_data,
        'has_next': page_obj.has_next(),
        'total_pages': paginator.num_pages
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


@login_required_buyer
def cart(request: HttpRequest):
    return render(request, "buyer/cart.html")


@login_required_buyer
def orders(request: HttpRequest):
    return render(request, "buyer/orders.html")


@login_required_buyer
def profile(request: HttpRequest):
    return render(request, "buyer/profile.html")


def page_not_found(request: HttpRequest, exception):
    return render(request, "buyer/404.html", status=404)
