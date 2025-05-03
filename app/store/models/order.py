from django.db import models
from django.conf import settings
from .user import User


class Cart(models.Model):
    buyer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.Role.SELLER}
    )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'role': User.Role.BUYER}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey('store.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.PositiveIntegerField()


class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('PAYMENT', 'Ожидание оплаты'),
        ('PROCESSING', 'В обработке'),
        ('SHIPPED', 'Отправлен'),
        ('TRANSIT', 'В пути'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменён'),
        ('RETURNED', 'Возвращён'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 related_name='delivery')
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=DELIVERY_STATUS_CHOICES,
                              default='PAYMENT')
    tracking_number = models.CharField(max_length=50)

