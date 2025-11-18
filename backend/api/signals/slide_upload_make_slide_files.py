import os
import logging
import traceback

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from api.models.slides import SlideModel
from .utils import make_thumbnail, make_dzi

logger = logging.getLogger(__name__)


@receiver(post_save, sender=SlideModel, dispatch_uid="slide_postsave_generate")
def process_slide_on_save(sender, instance, created, **kwargs):
    # If there’s no path, do nothing
    if not instance.svs_file:
        logger.warning(
            "Slide %s saved with no svs_file set; skipping conversion.",
            instance.pk,
        )
        return

    # Resolve to an absolute filesystem path
    svs_path = getattr(instance, "svs_abs_path", None) or instance.svs_file

    # If the file doesn't actually exist on disk, bail safely
    if not os.path.exists(svs_path):
        msg = f"[slide_postsave_generate] SVS not found on disk: {svs_path}"
        print(msg, flush=True)
        logger.error(msg)
        return

    stem = str(instance.id)  # single source of truth

    def _generate():
        try:
            os.makedirs(settings.THUMBNAIL_ROOT, exist_ok=True)
            os.makedirs(settings.DZI_ROOT, exist_ok=True)

            # ALWAYS (re)build — even if the filename didn't change
            logger.info("Generating thumbnail + DZI for slide %s (%s)", instance.pk, svs_path)
            make_thumbnail(svs_path, stem)
            make_dzi(svs_path, stem)

            # Persist paths (relative to MEDIA_ROOT)
            type(instance).objects.filter(pk=instance.pk).update(
                thumbnail_path=f"thumbnails/{stem}.jpeg",
                dzi_xml_path=f"dzi/{stem}.dzi",
                dzi_tiles_path=f"dzi/{stem}_files",
            )
            logger.info("Updated paths for slide %s", instance.pk)

        except Exception:
            # Log full traceback to gunicorn log
            logger.exception(
                "Error generating DZI/thumbnail for slide %s (%s)",
                instance.pk,
                svs_path,
            )
            # Also print so we get it even with minimal logging config
            traceback.print_exc()

    # Run after DB commit
    transaction.on_commit(_generate)