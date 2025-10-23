from django.contrib import admin
from .models import User, Order, Product, OrderItem
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.unregister(User)

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