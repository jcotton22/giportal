import os
import pyvips
import openslide
from django.conf import settings

def make_thumbnail(svs_path: str, slide_id: str):

    thumbnail_path = os.path.join(settings.THUMBNAIL_ROOT, f"{slide_id}.jpeg")
    slide = openslide.OpenSlide(svs_path)
    thumbnail = slide.get_thumbnail((256, 256))
    thumbnail.save(thumbnail_path, "JPEG")
    slide.close()

def make_dzi(svs_path: str, slide_id: str):

    dzi_path = os.path.join(settings.DZI_ROOT, f"{slide_id}")    
    image = pyvips.Image.new_from_file(svs_path, access='sequential')
    image.dzsave(dzi_path, tile_size=256, overlap=1, suffix='.jpeg')