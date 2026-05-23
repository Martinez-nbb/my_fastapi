import asyncio
import os

from src.core.exceptions.domain_exceptions import (
    ImageFolderNotFoundException,
    ImageFolderNotWritableException,
)


async def async_write_file(path: str, content: bytes) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _sync_write_file, path, content)


def _sync_write_file(path: str, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


async def async_read_file(path: str) -> bytes:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _sync_read_file, path)


def _sync_read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


async def async_path_exists(path: str) -> bool:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, os.path.exists, path)


async def async_remove_file(path: str) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _sync_remove_file, path)


def _sync_remove_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


async def async_check_folder(path: str) -> None:
    loop = asyncio.get_running_loop()

    def _check():
        if not os.path.exists(path):
            raise ImageFolderNotFoundException(f"Folder not found: {path}")
        if not os.access(path, os.W_OK):
            raise ImageFolderNotWritableException(f"Folder not writable: {path}")

    await loop.run_in_executor(None, _check)
