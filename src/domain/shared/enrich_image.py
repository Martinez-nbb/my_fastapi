import base64

from src.domain.shared.async_file import async_read_file, async_path_exists

MEDIA_TYPES = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}


def build_media_type(file_path: str) -> str:
    ext = file_path.rsplit('.', 1)[-1] if '.' in file_path else ''
    return MEDIA_TYPES.get(ext, "image/jpeg")


async def enrich_image_data(file_path: str, image_folder: str) -> str:
    full_path = f"{image_folder}/{file_path}"
    media_type = build_media_type(file_path)
    if await async_path_exists(full_path):
        raw = await async_read_file(full_path)
        return f"data:{media_type};base64,{base64.b64encode(raw).decode('utf-8')}"
    return ""
