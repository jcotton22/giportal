import os
import logging

import pyvips
import openslide
from django.conf import settings

logger = logging.getLogger(__name__)


def make_thumbnail(svs_path: str, slide_id: str, size=(256, 256)) -> None:
    """
    Create a JPEG thumbnail from an SVS slide.

    If OpenSlide can't handle the slide (e.g. ICC profile bug: "Array length must be >= 0"),
    we log the error and return without raising so the request doesn't 500.
    """
    thumbnail_path = os.path.join(settings.THUMBNAIL_ROOT, f"{slide_id}.jpeg")
    os.makedirs(settings.THUMBNAIL_ROOT, exist_ok=True)

    try:
        slide = openslide.OpenSlide(svs_path)
    except (ValueError, openslide.OpenSlideError) as e:
        # This catches the "Array length must be >= 0, not -1" ICC issue
        logger.exception("OpenSlide failed to open %s for thumbnail: %s", svs_path, e)
        return

    try:
        thumb = slide.get_thumbnail(size)
        thumb = thumb.convert("RGB")
        thumb.save(thumbnail_path, "JPEG")
        logger.info("Thumbnail written to %s", thumbnail_path)
    finally:
        slide.close()


def make_dzi(svs_path: str, slide_id: str) -> None:
    """
    Create DeepZoom (DZI) tiles using pyvips.

    Will write:
      - <DZI_ROOT>/<slide_id>.dzi
      - <DZI_ROOT>/<slide_id>_files/...
    """
    os.makedirs(settings.DZI_ROOT, exist_ok=True)
    dzi_base = os.path.join(settings.DZI_ROOT, slide_id)

    try:
        # libvips will usually use OpenSlide under the hood for SVS
        image = pyvips.Image.new_from_file(svs_path, access="sequential")
        image.dzsave(
            dzi_base,
            tile_size=256,
            overlap=1,
            suffix=".jpeg",
        )
        logger.info("DZI written with base %s (.dzi and _files/)", dzi_base)
    except pyvips.Error as e:
        logger.exception("pyvips failed to create DZI for %s: %s", svs_path, e)
        # Don't re-raise; we log and let the caller continue
        return