from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(max_length=7)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='photos')
    photo = models.ImageField(upload_to='product_photos/')
