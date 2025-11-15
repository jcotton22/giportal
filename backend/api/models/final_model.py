
import uuid
from django.db import models
from .base import BaseModel

class FinalModel(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    creation_date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Questions"
        verbose_name_plural = "Add question set"
        ordering = ('-creation_date',)

    def __str__(self):
        return f'New exam {self.id} created on {self.creation_date}'