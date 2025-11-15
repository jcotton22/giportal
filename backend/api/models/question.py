import uuid
from django.db import models

from .final_model import FinalModel

class QuestionModel(models.Model):
    question_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    clinical_information = models.TextField()
    question = models.CharField(max_length=250)
    exam = models.ForeignKey(         
        FinalModel,
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True,
    )

