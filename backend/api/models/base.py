
from django.db import models

from api.models.lookups import OrganSystem, StaffUploader

class BaseModel(models.Model):
    class ModelChoices(models.TextChoices):
        EXAM = 'E', 'Exam'
        UNKNOWNS = 'U', 'Unknown'
        GROSS = 'G', 'Gross'
    
    model_type = models.CharField(max_length=15, choices=ModelChoices.choices)
    organ_system = models.ForeignKey(
        OrganSystem,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
        null=True,
        blank=True
    )
    uploaded_by = models.ForeignKey(
        StaffUploader,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
