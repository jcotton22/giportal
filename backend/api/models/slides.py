import uuid
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.utils.text import slugify

from .question import QuestionModel


class SlideModel(models.Model):
    """
    A slide that points at pre-generated thumbnail + DZI assets.

    Canonical identity:
      - accession_no + slide_no  → stem (slug)  → relative paths under MEDIA_ROOT
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # ✅ allow slides to exist WITHOUT a question (import first, attach later)
    question = models.ForeignKey(
        QuestionModel,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )

    accession_no = models.CharField(max_length=20, help_text="APL accession number")
    slide_no = models.CharField(max_length=10)

    # Slug that we derive from accession_no + "-" + slide_no
    stem = models.SlugField(
        max_length=255,
        editable=False,
        blank=True,
        help_text="Auto-generated identifier from accession + slide",
    )

    # Description is the “primary source of truth” label you type
    description = models.TextField()

    # Relative to MEDIA_ROOT
    thumbnail_path = models.CharField(max_length=255, blank=True, default="")
    dzi_xml_path = models.CharField(max_length=255, blank=True, default="")
    dzi_tiles_path = models.CharField(max_length=255, blank=True, default="")

    def save(self, *args, **kwargs):
        """
        Make accession_no + slide_no the canonical identity of the slide.

        All file paths are derived from:
            stem = slugify(f"{accession_no}-{slide_no}")

        That stem MUST match what your offline converter used.
        """
        base = f"{self.accession_no}-{self.slide_no}"
        new_stem = slugify(base)  # e.g. "PLS24-005960-A3" → "pls24-005960-a3"

        if not self.stem or self.stem != new_stem:
            self.stem = new_stem
            self.thumbnail_path = f"thumbnails/{self.stem}.jpeg"
            self.dzi_xml_path = f"dzi/{self.stem}.dzi"
            self.dzi_tiles_path = f"dzi/{self.stem}_files"

        super().save(*args, **kwargs)

    # Convenience URLs via default_storage (FileSystemStorage on prod)
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
        return f"{self.accession_no} {self.slide_no}"