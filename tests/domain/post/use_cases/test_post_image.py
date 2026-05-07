import pytest
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from src.domain.post.use_cases.add_post_image import AddPostImageUseCase
from src.domain.post.use_cases.get_post_image import GetPostImageUseCase
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostHasNoImageException
from src.schemas.posts import PostImageResponse


class FakeUploadFile:
    def __init__(self, filename: str, content: bytes = b"fake image"):
        self.filename = filename
        self._content = content
        self._file = MagicMock()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
        
    @property
    def file(self):
        return self


class FakePost:
    def __init__(self, post_id: int, image: str | None = None):
        self.id = post_id
        self.image = image


class TestAddPostImageUseCase:
    @pytest.mark.asyncio
    async def test_uploads_jpeg_image(self, tmp_path):
        with patch('src.domain.post.use_cases.add_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1)
            MockRepo.return_value = mock_repo

            use_case = AddPostImageUseCase()
            use_case.image_folder = str(tmp_path)
            use_case._repo = mock_repo

            image = FakeUploadFile("test.jpeg")
            image._file.read = MagicMock(return_value=b"fake image data")

            with patch('builtins.open', mock_open()):
                result = await use_case.execute(post_id=1, image=image)

            assert isinstance(result, PostImageResponse)
            assert result.image_path.endswith(".jpeg")

    @pytest.mark.asyncio
    async def test_uploads_png_image(self):
        with patch('src.domain.post.use_cases.add_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1)
            MockRepo.return_value = mock_repo

            use_case = AddPostImageUseCase()
            use_case._repo = mock_repo
            use_case.image_folder = "/tmp/test"

            image = FakeUploadFile("test.png")

            with patch('builtins.open', mock_open()):
                result = await use_case.execute(post_id=1, image=image)

            assert isinstance(result, PostImageResponse)
            assert result.image_path.endswith(".png")

    @pytest.mark.asyncio
    async def test_raises_when_post_not_found(self):
        with patch('src.domain.post.use_cases.add_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = None
            MockRepo.return_value = mock_repo

            use_case = AddPostImageUseCase()
            use_case._repo = mock_repo

            image = FakeUploadFile("test.jpeg")

            with pytest.raises(PostNotFoundException):
                await use_case.execute(post_id=999, image=image)

    @pytest.mark.asyncio
    async def test_raises_for_invalid_extension(self):
        with patch('src.domain.post.use_cases.add_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1)
            MockRepo.return_value = mock_repo

            use_case = AddPostImageUseCase()
            use_case._repo = mock_repo

            image = FakeUploadFile("test.gif")

            with pytest.raises(ValueError, match="Image must be JPEG or PNG"):
                await use_case.execute(post_id=1, image=image)

    @pytest.mark.asyncio
    async def test_raises_for_missing_filename(self):
        with patch('src.domain.post.use_cases.add_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1)
            MockRepo.return_value = mock_repo

            use_case = AddPostImageUseCase()
            use_case._repo = mock_repo

            image = FakeUploadFile("")

            with pytest.raises(ValueError, match="Image must be JPEG or PNG"):
                await use_case.execute(post_id=1, image=image)


class TestGetPostImageUseCase:
    @pytest.mark.asyncio
    async def test_returns_jpeg_image(self):
        with patch('src.domain.post.use_cases.get_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1, image="test.jpeg")
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo
            use_case.image_folder = "/nonexistent"

            result = await use_case.execute(post_id=1)

            assert result.media_type == "image/jpeg"

    @pytest.mark.asyncio
    async def test_raises_when_post_not_found(self):
        with patch('src.domain.post.use_cases.get_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = None
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo

            with pytest.raises(PostNotFoundException):
                await use_case.execute(post_id=999)

    @pytest.mark.asyncio
    async def test_raises_when_post_has_no_image(self):
        with patch('src.domain.post.use_cases.get_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1, image=None)
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo

            with pytest.raises(PostHasNoImageException):
                await use_case.execute(post_id=1)

    @pytest.mark.asyncio
    async def test_returns_png_image(self):
        with patch('src.domain.post.use_cases.get_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1, image="test.png")
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo
            use_case.image_folder = "/nonexistent"

            result = await use_case.execute(post_id=1)

            assert result.media_type == "image/png"

    @pytest.mark.asyncio
    async def test_returns_jpg_image(self):
        with patch('src.domain.post.use_cases.get_post_image.PostRepository') as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get.return_value = FakePost(id=1, image="test.jpg")
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo
            use_case.image_folder = "/nonexistent"

            result = await use_case.execute(post_id=1)

            assert result.media_type == "image/jpeg"