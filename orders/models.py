from django.db import models
from django.contrib.auth.models import User
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Product(BaseModel):
    name = models.CharField(
        max_length=255,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.name}'
    
        
class Order(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Client'
    )
    
    code = models.CharField(max_length = 15, unique = True, blank=True)
    
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        through='OrderItem'
    )
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(self.id).replace('-', '')[:15].lower()
        super().save(*args, **kwargs)
    
    @property
    def total_amount(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f'{self.code}'
    
class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    def __str__(self):
        return f"{self.product.name} (Order {self.order.code})"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity

