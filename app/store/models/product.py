from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from .user import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'role': User.Role.SELLER})
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    @property
    def average_rating(self):
        result = self.reviews.aggregate(average=Avg('rating'))
        return result['average'] if result['average'] is not None else 0

    @property
    def reviews_count(self):
        return self.reviews.count()

    @property
    def seller_username(self):
        return self.seller.username

    @property
    def primary_photo(self):
        return self.photos.filter(is_primary=True).first()


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField(upload_to='product_photos/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'Фото товара {self.product.name}'

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.Role.BUYER}
    )
    rating = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        default=0
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв покупателя {self.buyer.username} на товар \
                {self.product.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
