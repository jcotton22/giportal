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

    # SSH-uploaded slides live under settings.SVS_SLIDE_ROOT
    svs_file = models.FilePathField(
        path=settings.SVS_SLIDE_ROOT,
        match=r".*\.svs$",
        recursive=True,
        allow_files=True,
        allow_folders=False,
        max_length=500,
    )

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

    @property
    def svs_abs_path(self) -> str:
        """
        Absolute filesystem path to the SVS file.

        For FilePathField this will usually already be absolute, but this
        keeps it robust if you ever store relative paths.
        """
        p = self.svs_file or ""
        if os.path.isabs(p):
            return p
        return os.path.join(settings.SVS_SLIDE_ROOT, p)