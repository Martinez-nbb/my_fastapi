"""
Исключения уровня базы данных.

Эти исключения используются инфраструктурой (репозиториями) для сигнализации
о проблемах при работе с базой данных. Они транслируются в domain_exceptions
на уровне use case.
"""


class BaseDatabaseException(Exception):
    """Базовое исключение для ошибок базы данных."""

    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseException):
    """Пользователь не найден в базе данных."""

    pass


class UserAlreadyExistsException(BaseDatabaseException):
    """Пользователь с таким логином/email уже существует."""

    pass


class CategoryNotFoundException(BaseDatabaseException):
    """Категория не найдена в базе данных."""

    pass


class CategorySlugAlreadyExistsException(BaseDatabaseException):
    """Категория с таким slug уже существует."""

    pass


class LocationNotFoundException(BaseDatabaseException):
    """Местоположение не найдено в базе данных."""

    pass


class PostNotFoundException(BaseDatabaseException):
    """Публикация не найдена в базе данных."""

    pass


class CommentNotFoundException(BaseDatabaseException):
    """Комментарий не найден в базе данных."""

    pass


class AuthorNotFoundException(BaseDatabaseException):
    """Автор не найден в базе данных."""

    pass
