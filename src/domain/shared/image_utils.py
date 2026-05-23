from fastapi import UploadFile

from src.core.exceptions.domain_exceptions import UploadFileIsNotImageException
from src.core.logging import get_logger

logger = get_logger(__name__)

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image(image: UploadFile) -> str:
    if not hasattr(image, 'filename') or not image.filename:
        logger.warning("Отсутствует имя файла")
        raise ValueError("Filename is required")

    filename = image.filename.lower()
    ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''

    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Невалидное расширение файла: ext={ext}, filename={filename}")
        raise UploadFileIsNotImageException()

    return ext
