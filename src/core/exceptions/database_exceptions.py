from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseException):
    pass


class UserUsernameAlreadyExistsException(BaseDatabaseException):
    pass


class UserEmailAlreadyExistsException(BaseDatabaseException):
    pass


class CategoryNotFoundException(BaseDatabaseException):
    pass


class CategorySlugAlreadyExistsException(BaseDatabaseException):
    pass


class LocationNotFoundException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class CommentNotFoundException(BaseDatabaseException):
    pass


class DatabaseConnectionError(BaseDatabaseException):
    pass


class DatabaseIntegrityError(BaseDatabaseException):
    pass


class DatabaseOperationalError(BaseDatabaseException):
    pass


def handle_database_exception(exc: SQLAlchemyError, entity: str = 'Запись') -> BaseDatabaseException:
    if isinstance(exc, IntegrityError):
        if 'username' in str(exc.orig).lower():
            return UserUsernameAlreadyExistsException('Имя пользователя уже существует')
        if 'email' in str(exc.orig).lower():
            return UserEmailAlreadyExistsException('Email уже существует')
        if 'slug' in str(exc.orig).lower():
            return CategorySlugAlreadyExistsException('Slug уже существует')
        return DatabaseIntegrityError(f'Нарушение целостности базы данных при работе с сущностью {entity}')
    
    if isinstance(exc, DatabaseOperationalError):
        return DatabaseConnectionError(f'Ошибка подключения к базе данных: {exc}')
    
    return BaseDatabaseException(f'Ошибка базы данных при работе с сущностью {entity}: {exc}')
