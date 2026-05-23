import io
import os
import logging

from PIL import Image

logger = logging.getLogger(__name__)


def combine_images_vertically(file_paths: list[str], image_folder: str) -> io.BytesIO:
    images = []
    for fp in file_paths:
        full_path = os.path.join(image_folder, fp)
        if not os.path.exists(full_path):
            continue
        try:
            img = Image.open(full_path)
            img.load()
            if img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
        except Exception as exc:
            logger.warning("Skipping image %s: %s", fp, exc)

    if not images:
        raise FileNotFoundError("No valid images found")

    total_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    canvas = Image.new("RGB", (total_width, total_height), (255, 255, 255))
    y_offset = 0
    for img in images:
        canvas.paste(img, (0, y_offset))
        y_offset += img.height

    buf = io.BytesIO()
    canvas.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return buf
