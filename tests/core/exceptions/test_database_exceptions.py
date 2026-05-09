import pytest

from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    CommentNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserUsernameOrEmailIsNotUniqueException,
    PostNotFoundByIdException,
    CategoryNotFoundByIdException,
    CategoryNotFoundBySlugException,
    LocationNotFoundByIdException,
    CommentNotFoundByIdException,
    PostHasNoImageException,
    UploadFileIsNotImageException,
)
from src.core.exceptions.auth_exceptions import (
    CredentialsException,
    InvalidTokenException,
)


class TestDatabaseExceptions:
    def test_user_not_found_exception(self):
        exc = UserNotFoundException()
        assert exc.args[0] is not None

    def test_user_username_already_exists_exception(self):
        exc = UserUsernameAlreadyExistsException()
        assert exc.args[0] is not None

    def test_user_email_already_exists_exception(self):
        exc = UserEmailAlreadyExistsException()
        assert exc.args[0] is not None

    def test_post_not_found_exception(self):
        exc = PostNotFoundException()
        assert exc.args[0] is not None

    def test_category_not_found_exception(self):
        exc = CategoryNotFoundException()
        assert exc.args[0] is not None

    def test_location_not_found_exception(self):
        exc = LocationNotFoundException()
        assert exc.args[0] is not None

    def test_comment_not_found_exception(self):
        exc = CommentNotFoundException()
        assert exc.args[0] is not None


class TestDomainExceptions:
    def test_user_not_found_by_id_exception(self):
        exc = UserNotFoundByIdException(id=42)
        assert "42" in exc.get_detail()

    def test_user_not_found_by_username_exception(self):
        exc = UserNotFoundByUsernameException(username="testuser")
        assert "testuser" in exc.get_detail()

    def test_user_not_unique_exception_from_username(self):
        exc = UserUsernameOrEmailIsNotUniqueException.from_username(username="duplicate")
        assert "duplicate" in exc.get_detail()

    def test_user_not_unique_exception_from_email(self):
        exc = UserUsernameOrEmailIsNotUniqueException.from_email(email="test@test.com")
        assert "test@test.com" in exc.get_detail()

    def test_post_not_found_by_id_exception(self):
        exc = PostNotFoundByIdException(id=10)
        assert "10" in exc.get_detail()

    def test_category_not_found_by_id_exception(self):
        exc = CategoryNotFoundByIdException(id=5)
        assert "5" in exc.get_detail()

    def test_category_not_found_by_slug_exception(self):
        exc = CategoryNotFoundBySlugException(slug="tech")
        assert "tech" in exc.get_detail()

    def test_location_not_found_by_id_exception(self):
        exc = LocationNotFoundByIdException(id=3)
        assert "3" in exc.get_detail()

    def test_comment_not_found_by_id_exception(self):
        exc = CommentNotFoundByIdException(id=7)
        assert "7" in exc.get_detail()

    def test_post_has_no_image_exception(self):
        exc = PostHasNoImageException(post_id=42)
        assert "42" in exc.get_detail()
        assert exc.post_id == 42

    def test_upload_file_is_not_image_exception(self):
        exc = UploadFileIsNotImageException()
        assert "JPEG" in exc.get_detail()


class TestAuthExceptions:
    def test_credentials_exception(self):
        from fastapi import HTTPException, status
        exc = CredentialsException(detail="Invalid credentials")
        assert exc.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.detail == "Invalid credentials"

    def test_invalid_token_exception(self):
        from fastapi import HTTPException, status
        exc = InvalidTokenException(detail="Token expired")
        assert exc.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.detail == "Token expired"