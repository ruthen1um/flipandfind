from django.db import models


class Card(models.Model):
    number = models.CharField(max_length=19, unique=True)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'


class Payment(models.Model):
    order = models.ForeignKey('store.Order', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Платёж по заказу покупателя {self.order.buyer.username}'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
