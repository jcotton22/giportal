import traceback
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=SlideModel, dispatch_uid="slide_postsave_generate")
def process_slide_on_save(sender, instance, created, **kwargs):
    if not instance.svs_file:
        return

    svs_path = getattr(instance, "svs_abs_path", None) or instance.svs_file

    if not os.path.exists(svs_path):
        print(f"[slide_postsave_generate] SVS not found on disk: {svs_path}", flush=True)
        return

    stem = str(instance.id)

    def _generate():
        try:
            os.makedirs(settings.THUMBNAIL_ROOT, exist_ok=True)
            os.makedirs(settings.DZI_ROOT, exist_ok=True)

            make_thumbnail(svs_path, stem)
            make_dzi(svs_path, stem)

            type(instance).objects.filter(pk=instance.pk).update(
                thumbnail_path=f"thumbnails/{stem}.jpeg",
                dzi_xml_path=f"dzi/{stem}.dzi",
                dzi_tiles_path=f"dzi/{stem}_files",
            )
        except Exception:
            logger.exception("Error generating DZI/thumbnail for slide %s (%s)", instance.pk, svs_path)
            traceback.print_exc()

    transaction.on_commit(_generate)