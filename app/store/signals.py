from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Cart


@receiver(post_save, sender=User)
def create_cart_for_buyer(sender, instance, created, **kwargs):
    if instance.role == 'BUYER' and created:
        Cart.objects.get_or_create(buyer=instance)
