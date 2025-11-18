import os
import uuid
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.text import slugify

from .question import QuestionModel

class SlideModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    question = models.ForeignKey(
        "QuestionModel",
        on_delete=models.CASCADE,
        related_name="files",
    )

    accession_no = models.CharField(max_length=20, help_text='APL Accession Number')
    slide_no = models.CharField(max_length=10)

    stem = models.SlugField(
        max_length=255,
        editable=False,
        blank=True,
        help_text="Auto generated identifier from acccession number"
    )

    description = models.TextField()

    thumbnail_path = models.CharField(max_length=255, blank=True, default="")
    dzi_xml_path   = models.CharField(max_length=255, blank=True, default="")
    dzi_tiles_path = models.CharField(max_length=255, blank=True, default="")

    def save(self, *args, **kwargs):
        """
            Make Accession number and slide number the canonical identity of the slide
            All file paths being derived from slugified description
        """

        new_stem = slugify(self.accession_no + self.slide_no)

        if not self.stem or self.stem != new_stem:
            self.stem = new_stem
            self.thumbnail_path = f"thumbnails/{self.stem}.jpeg"
            self.dzi_xml_path = f"dzi/{self.stem}.dzi"
            self.dzi_tiles_path = f"dzi/{self.stem}_files"

        super().save(*args, **kwargs)

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

    def __str__(self):
        return f"{self.accession_no} + {self.slide_no}"
    