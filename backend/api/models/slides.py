import os
import uuid
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from .question import QuestionModel


class SlideModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    question = models.ForeignKey(
        "QuestionModel",
        on_delete=models.CASCADE,
        related_name="files",
    )

    accession_no = models.CharField(
        max_length=20,
        help_text="APL Accession Number",
        blank=True,
    )
    slide_no = models.CharField(
        max_length=10,
        blank=True,
    )

    # Stem = the canonical key that matches your converted files
    # e.g. "pls24-005960-a3"
    stem = models.SlugField(
        max_length=255,
        editable=False,   # we set it from admin form logic
        blank=True,
        help_text="Internal key matching converted files (thumbnails/DZI).",
    )

    description = models.TextField(
        help_text="Description of what this slide/file set is.",
        blank=True,
    )

    thumbnail_path = models.CharField(max_length=255, blank=True, default="")
    dzi_xml_path   = models.CharField(max_length=255, blank=True, default="")
    dzi_tiles_path = models.CharField(max_length=255, blank=True, default="")

    def save(self, *args, **kwargs):
        """
        Use `stem` as single source of truth for file locations.
        Admin form will set `stem` to match a real DZI file on disk.
        """
        if self.stem:
            self.thumbnail_path = f"thumbnails/{self.stem}.jpeg"
            self.dzi_xml_path   = f"dzi/{self.stem}.dzi"
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
        label = f"{self.accession_no} {self.slide_no}".strip()
        return label or str(self.id)