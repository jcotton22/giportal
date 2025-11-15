import uuid
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def svs_upload_to(instance, filename):
    ext = Path(filename).suffix.lower() or ".svs"
    if not getattr(instance, "id", None):
        instance.id = uuid.uuid4()
    return f"svs_slide/{instance.id}{ext}"