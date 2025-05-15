from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from store.models import User, Cart, CartItem
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


def api_catalog(request):
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
def cart(request):
    try:
        cart_items = request.user.cart.items.select_related('product').all()
    except Cart.DoesNotExist:
        cart_items = []

    total_price = 0
    extended_cart_items = []

    for item in cart_items:
        line_total = item.product.price * item.quantity
        extended_cart_items.append({
            'id': item.id,
            'product_id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'line_total': line_total,
            'photo_url': item.product.primary_photo.url if item.product.primary_photo else None
        })
        total_price += line_total

    context = {
        'cart_items': extended_cart_items,
        'total_price': total_price,
        'item_count': len(extended_cart_items)
    }

    return render(request, "buyer/cart.html", context)


@login_required_buyer
def orders(request: HttpRequest):
    return render(request, "buyer/orders.html")


@login_required_buyer
def profile(request: HttpRequest):
    return render(request, "buyer/profile.html")


def page_not_found(request: HttpRequest, exception):
    return render(request, "buyer/404.html", status=404)


@login_required_buyer
@require_http_methods(["POST"])
def api_add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(buyer=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        "status": "ok",
        "quantity": cart_item.quantity,
        "line_total": cart_item.product.price * cart_item.quantity
    })


@login_required_buyer
@require_http_methods(["POST"])
def api_remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(buyer=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        return JsonResponse({"status": "ok"})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "error", "message": "Item not found"}, status=404)


@login_required_buyer
@require_http_methods(["POST"])
def api_update_quantity(request, product_id):
    quantity = int(request.POST.get("quantity", 1))
    cart = request.user.cart
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({"status": "deleted"})
    else:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({
            "status": "ok",
            "quantity": cart_item.quantity,
            "line_total": cart_item.product.price * cart_item.quantity
        })
