from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.expressions import CombinedExpression
from .models import Product

LOW_STOCK_THRESHOLD = 5

@receiver(post_save, sender=Product)
def alert_low_stock(sender, instance, **kwargs):
    # Skip check if stock is an expression (F() update)
    if isinstance(instance.stock, CombinedExpression):
        return

    if instance.stock is not None and instance.stock <= LOW_STOCK_THRESHOLD:
        print(f"[Alert] Low stock: '{instance.name}' has only {instance.stock} left!")
