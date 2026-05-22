import pytest
from unittest.mock import AsyncMock, patch

from src.domain.post.use_cases.add_post_image import AddPostImageUseCase
from src.domain.post.use_cases.get_post_image import GetPostImageUseCase
from src.core.exceptions.database_exceptions import PostImageNotFoundException
from src.core.exceptions.domain_exceptions import UploadFileIsNotImageException


class FakeUploadFile:
    def __init__(self, filename: str):
        self.filename = filename


class FakePostImage:
    def __init__(self, image_id: int, post_id: int, file_path: str):
        self.id = image_id
        self.post_id = post_id
        self.file_path = file_path


class TestAddPostImageUseCaseValidation:
    def test_accepts_jpg_extension(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("test.jpg")

        ext = use_case._validate_image(image)
        assert ext == "jpg"

    def test_accepts_png_extension(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("test.png")

        ext = use_case._validate_image(image)
        assert ext == "png"

    def test_accepts_gif_extension(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("test.gif")

        ext = use_case._validate_image(image)
        assert ext == "gif"

    def test_accepts_webp_extension(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("test.webp")

        ext = use_case._validate_image(image)
        assert ext == "webp"

    def test_raises_for_no_extension(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("test")

        with pytest.raises(UploadFileIsNotImageException):
            use_case._validate_image(image)

    def test_accepts_jpeg_extension(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("test.jpeg")

        ext = use_case._validate_image(image)
        assert ext == "jpeg"

    def test_raises_for_empty_filename(self):
        use_case = AddPostImageUseCase()
        image = FakeUploadFile("")

        with pytest.raises(ValueError):
            use_case._validate_image(image)


class TestGetPostImageUseCase:
    @pytest.mark.asyncio
    async def test_returns_jpeg_image(self):
        with patch('src.domain.post.use_cases.get_post_image.PostImageRepository') as MockRepo:
            mock_repo = AsyncMock()
            mock_repo.get.return_value = FakePostImage(1, 1, "test-uuid.jpeg")
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo

            with patch('os.path.exists', return_value=True):
                result = await use_case.execute(image_id=1)

            assert result.media_type == "image/jpeg"

    @pytest.mark.asyncio
    async def test_raises_when_image_not_found(self):
        with patch('src.domain.post.use_cases.get_post_image.PostImageRepository') as MockRepo:
            mock_repo = AsyncMock()
            mock_repo.get.side_effect = PostImageNotFoundException()
            MockRepo.return_value = mock_repo

            use_case = GetPostImageUseCase()
            use_case._repo = mock_repo

            with pytest.raises(PostImageNotFoundException):
                await use_case.execute(image_id=999)
