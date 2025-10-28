from django.db import models
import uuid

class OutboxEvent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    processed = models.BooleanField(default=False)
    body = models.JSONField()
    
    def __str__(self):
        return f'{self.id} - {self.body}'

