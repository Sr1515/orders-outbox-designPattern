from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Order
from outbox.models import OutboxEvent

@receiver(post_save, sender=Order)
def create_outbox_event(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        try:
            with transaction.atomic():
                if not OutboxEvent.objects.filter(body__order_id=str(instance.id)).exists():
                    body = {
                        "order_id": str(instance.id),
                        "user_id": instance.user.id,
                        "total_amount": float(instance.total_amount),
                        "items": [
                            {
                                "product_id": str(item.product.id),
                                "quantity": float(item.quantity)
                            }
                            for item in instance.items.all()
                        ]
                    }
                    OutboxEvent.objects.create(body=body)
        except Exception as e:
            raise e
