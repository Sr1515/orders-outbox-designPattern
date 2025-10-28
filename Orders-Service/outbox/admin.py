from django.contrib import admin
from .models import OutboxEvent

@admin.register(OutboxEvent)
class OutboxAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'processed',
        'body'
    )
    search_fields = ('processed',)
    list_filter = ('processed',)