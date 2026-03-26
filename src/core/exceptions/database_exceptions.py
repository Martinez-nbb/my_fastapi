class BaseDatabaseException(Exception):
    """Базовое исключение для ошибок базы данных."""

    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseException):
    """Пользователь не найден в базе данных."""

    pass


class UserUsernameAlreadyExistsException(BaseDatabaseException):
    """Пользователь с таким именем уже существует."""

    pass


class UserEmailAlreadyExistsException(BaseDatabaseException):
    """Пользователь с таким email уже существует."""

    pass


class CategoryNotFoundException(BaseDatabaseException):
    """Категория не найдена в базе данных."""

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
