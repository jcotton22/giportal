# api/signals/slide_postsave_generate.py
import os
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from api.models.slides import SlideModel
from .utils import make_thumbnail, make_dzi

@receiver(post_save, sender=SlideModel, dispatch_uid="slide_postsave_generate")
def process_slide_on_save(sender, instance, created, **kwargs):
    # If there’s no file, do nothing
    if not instance.svs_file:
        return

    stem = str(instance.id)  # single source of truth

    def _generate():
        os.makedirs(settings.THUMBNAIL_ROOT, exist_ok=True)
        os.makedirs(settings.DZI_ROOT, exist_ok=True)

        # ALWAYS (re)build — even if the filename didn't change
        make_thumbnail(instance.svs_file.path, stem)
        make_dzi(instance.svs_file.path, stem)

        # Persist paths (relative to MEDIA_ROOT)
        type(instance).objects.filter(pk=instance.pk).update(
            thumbnail_path=f"thumbnails/{stem}.jpeg",
            dzi_xml_path=f"dzi/{stem}.dzi",
            dzi_tiles_path=f"dzi/{stem}_files",
        )

    # Run after DB commit (safe with ATOMIC_REQUESTS/admin)
    transaction.on_commit(_generate)
