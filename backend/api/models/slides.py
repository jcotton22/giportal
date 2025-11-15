import uuid
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage

from .question import QuestionModel
from api.utils.svs_upload_to import svs_upload_to


def thumbnail_artifact_path(instance, filename):
    return f"thumbnails/{instance.id}.jpeg"

def dzi_path(instance, filename):
    return f"dzi/{instance.id}.dzi"

def dzi_folder(instance, filename):
    return f"dzi/{instance.id}_files"

class SlideModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey(
        "QuestionModel",        # string reference, no import needed
        on_delete=models.CASCADE,
        related_name="files",
    )
    svs_file = models.FileField(
        upload_to=svs_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=["svs"])],
    )

    # stored relative paths for artifacts
    thumbnail_path = models.CharField(max_length=255, blank=True, default="")
    dzi_xml_path   = models.CharField(max_length=255, blank=True, default="")
    dzi_tiles_path = models.CharField(max_length=255, blank=True, default="")

    @property
    def thumbnail_url(self) -> str:
        p = self.thumbnail_path
        return default_storage.url(p) if p and default_storage.exists(p) else ""

    @property
    def dzi_xml_url(self) -> str:
        p = self.dzi_xml_path
        return default_storage.url(p) if p and default_storage.exists(p) else ""

    @property
    def dzi_tiles_url(self) -> str:
        p = self.dzi_tiles_path
        return default_storage.url(p) if p and default_storage.exists(p) else ""
