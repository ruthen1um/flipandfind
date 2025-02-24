from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000000)
        ]
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='photos')
    photo = models.ImageField(upload_to='product_photos/')
