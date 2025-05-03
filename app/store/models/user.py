from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = 'BUYER', 'Buyer'
        SELLER = 'SELLER', 'Seller'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # Отчество может отсутствовать поэтому blank=True
    middle_name = models.CharField(max_length=30, blank=True)


class BuyerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=20, unique=True)
    card = models.OneToOneField('store.Card', on_delete=models.CASCADE)


class SellerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    tax_id = models.CharField(max_length=12, unique=True)
    rating = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        default=0
    )
    card = models.OneToOneField('store.Card', on_delete=models.CASCADE)
