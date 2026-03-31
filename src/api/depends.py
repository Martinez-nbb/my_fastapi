from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase

from src.domain.category.use_cases.get_category import GetCategoryUseCase
from src.domain.category.use_cases.list_categories import GetCategoriesUseCase
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase

from src.domain.location.use_cases.get_location import GetLocationUseCase
from src.domain.location.use_cases.list_locations import GetLocationsUseCase
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase

from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.list_posts import GetPostsUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase

from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.list_comments import GetCommentsUseCase, GetCommentsByPostUseCase
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase


def get_user_use_case() -> GetUserUseCase:
    return GetUserUseCase()


def get_users_use_case() -> GetUsersUseCase:
    return GetUsersUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()


def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()


def get_category_use_case() -> GetCategoryUseCase:
    return GetCategoryUseCase()


def get_categories_use_case() -> GetCategoriesUseCase:
    return GetCategoriesUseCase()


def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def update_category_use_case() -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase()


def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()


def get_location_use_case() -> GetLocationUseCase:
    return GetLocationUseCase()


def get_locations_use_case() -> GetLocationsUseCase:
    return GetLocationsUseCase()


def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


def update_location_use_case() -> UpdateLocationUseCase:
    return UpdateLocationUseCase()


def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def get_post_use_case() -> GetPostUseCase:
    return GetPostUseCase()


def get_posts_use_case() -> GetPostsUseCase:
    return GetPostsUseCase()


def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_comment_use_case() -> GetCommentUseCase:
    return GetCommentUseCase()


def get_comments_use_case() -> GetCommentsUseCase:
    return GetCommentsUseCase()


def get_comments_by_post_use_case() -> GetCommentsByPostUseCase:
    return GetCommentsByPostUseCase()


def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


def update_comment_use_case() -> UpdateCommentUseCase:
    return UpdateCommentUseCase()


def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()
