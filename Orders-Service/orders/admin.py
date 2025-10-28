from django.contrib import admin
from django import forms
from django.contrib.admin import widgets
from .models import User, Order, Product, OrderItem
from django.contrib.auth.admin import UserAdmin
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import Order
from outbox.models import OutboxEvent

admin.site.unregister(User)

class OrderForm(forms.ModelForm):
    order_items = forms.ModelMultipleChoiceField(
        queryset=OrderItem.objects.all(),
        widget = widgets.FilteredSelectMultiple('products', is_stacked=False)
    )
    
    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
            for order_item in self.cleaned_data.get('order_items', []):
                if order_item.order != order:
                    order_item.order = order
                    order_item.save()
        return order
    
    class Meta:
        model = Order
        fields = '__all__'
    
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
    )
    list_filter = ('is_active', 'is_staff',)
    search_fields = ('username', 'email',)
    
    fieldsets = (
    ('Informations', {
        "fields": ('id', 'email'),
    }),
    
    (_('Credentials'), {
        "fields": ('username', 'password'),
    }),
    
    (_('Groups and Permissions'), {
        "fields": ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
)
        
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "nome",
                    "login",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    readonly_fields = (
        "id",
    )
       
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'created_at',
        'updated_at',
    )
    search_fields = ('name', 'price',)
    list_filter = ('name',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'code',
        'created_at',
        'updated_at',
        'display_total_amount',
    )
    search_fields = ('code',)
    list_filter = ('code',)
    
    form = OrderForm
    
    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            created = super().save_model(request, obj, form, change)

            for order_item in form.cleaned_data.get('order_items', []):
                if order_item.order != obj:
                    order_item.order = obj
                    order_item.save()

            items_data = [
                {
                    "product_id": str(item.product.id),
                    "quantity": float(item.quantity),
                }
                for item in obj.items.all()
            ]

            body = {
                "order_id": str(obj.id),
                "user_id": obj.user.id,
                "total_amount": float(obj.total_amount),
                "items": items_data
            }

            OutboxEvent.objects.create(body=body)

        return created
    
    @admin.display(description='Total_Amount')
    def display_total_amount(self, obj):
        return obj.total_amount

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'created_at',
        'updated_at',
    )
    search_fields = ('order',)
    list_filter = ('order',)