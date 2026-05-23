import pytest
from datetime import datetime
from pydantic import ValidationError

from src.schemas.posts import (
    PostResponseSchema,
    PostCreateSchema,
    PostUpdateSchema,
)
from src.schemas.users import UserResponseSchema


class TestPostResponseSchema:
    def test_create_post_response_schema(self):
        """Тест создания схемы поста."""
        user = UserResponseSchema(
            id=1,
            username="author",
            first_name="Author",
            last_name="Name",
            email="author@test.com",
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )

        data = {
            "id": 1,
            "title": "Test Post",
            "text": "Post content",
            "pub_date": datetime.now(),
            "is_published": True,
            "author": user,
            "category": None,
            "location": None,
            "created_at": datetime.now(),
        }

        schema = PostResponseSchema(**data)

        assert schema.title == "Test Post"
        assert schema.text == "Post content"
        assert schema.is_published is True

    def test_post_with_category_and_location(self):
        """Тест поста с категорией и локацией."""
        user = UserResponseSchema(
            id=1,
            username="author",
            first_name="Author",
            last_name="Name",
            email="author@test.com",
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )

        data = {
            "id": 1,
            "title": "Test",
            "text": "Content",
            "pub_date": datetime.now(),
            "is_published": True,
            "author": user,
            "category": {"id": 1, "title": "Tech", "slug": "tech", "description": "Technology"},
            "location": {"id": 1, "name": "Moscow"},
            "created_at": datetime.now(),
        }

        schema = PostResponseSchema(**data)

        assert schema.category is not None
        assert schema.location is not None


class TestPostCreateSchema:
    def test_create_post_with_required_fields(self):
        """Тест создания поста с обязательными полями."""
        data = {
            "title": "New Post",
            "text": "Content here",
            "author_id": 1,
            "pub_date": datetime.now(),
        }

        schema = PostCreateSchema(**data)

        assert schema.title == "New Post"
        assert schema.text == "Content here"
        assert schema.author_id == 1

    def test_create_post_with_all_fields(self):
        """Тест создания поста со всеми полями."""
        data = {
            "title": "Full Post",
            "text": "Full content",
            "author_id": 1,
            "pub_date": datetime.now(),
            "category_id": 1,
            "location_id": 2,
            "is_published": False,
        }

        schema = PostCreateSchema(**data)

        assert schema.title == "Full Post"
        assert schema.category_id == 1
        assert schema.location_id == 2
        assert schema.is_published is False


class TestPostUpdateSchema:
    def test_create_update_schema(self):
        """Тест схемы обновления поста."""
        data = {
            "title": "Updated Title",
            "is_published": False,
        }

        schema = PostUpdateSchema(**data)

        assert schema.title == "Updated Title"
        assert schema.is_published is False

    def test_partial_update(self):
        """Тест частичного обновления."""
        schema = PostUpdateSchema(is_published=True)

        assert schema.is_published is True
        assert schema.title is None


