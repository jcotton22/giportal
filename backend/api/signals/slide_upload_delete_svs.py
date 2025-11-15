import os
import shutil
from django.db import transaction
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

from api.models.slides import SlideModel

def _purge_stem(stem: str):
    try:
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f'{stem}.jpeg')
        dzi_dir = os.path.join(settings.MEDIA_ROOT, 'dzi', f'{stem}_files')
        dzi_xml = os.path.join(settings.MEDIA_ROOT, 'dzi', f'{stem}.dzi')
        if os.path.exists(thumbnail_path): os.remove(thumbnail_path)
        if os.path.exists(dzi_xml): os.remove(dzi_xml)
        if os.path.exists(dzi_dir): shutil.rmtree(dzi_dir, ignore_errors=True)
    except Exception as e:
        print(f"Error purging artifacts for stem={stem}: {e}", flush=True)

@receiver(post_delete, sender=SlideModel, dispatch_uid="slide_postdelete_cleanup")
def cleanup_slide_on_delete(sender, instance, **kwargs):
    svs_name = (instance.svs_file.name or "").strip()

    stems = {
        instance.id,
    }

    def _cleanup():
        if svs_name:
            try:
                instance.svs_file.storage.delete(svs_name)
            except Exception as e:
                print(f"Error deleting SVS '{svs_name}' for slide {instance.pk}: {e}", flush=True)
        for stem in stems:
            _purge_stem(stem)

    transaction.on_commit(_cleanup)
  