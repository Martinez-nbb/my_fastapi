from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError


class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail
        self.error_type = self.__class__.__name__


class UserNotFoundException(BaseDatabaseException):
    def __init__(self, user_id: int | None = None, username: str | None = None) -> None:
        if user_id is not None:
            detail = f'Пользователь с идентификатором {user_id} не найден в базе данных'
        elif username is not None:
            detail = f'Пользователь с именем "{username}" не найден в базе данных'
        else:
            detail = 'Пользователь не найден в базе данных'
        super().__init__(detail=detail)


class UserUsernameAlreadyExistsException(BaseDatabaseException):
    def __init__(self, username: str) -> None:
        detail = f'Пользователь с именем "{username}" уже существует в базе данных. Выберите другое имя'
        super().__init__(detail=detail)


class UserEmailAlreadyExistsException(BaseDatabaseException):
    def __init__(self, email: str) -> None:
        detail = f'Пользователь с email "{email}" уже существует в базе данных. Используйте другой email'
        super().__init__(detail=detail)


class CategoryNotFoundException(BaseDatabaseException):
    def __init__(self, category_id: int | None = None, slug: str | None = None) -> None:
        if category_id is not None:
            detail = f'Категория с идентификатором {category_id} не найдена в базе данных'
        elif slug is not None:
            detail = f'Категория со slug "{slug}" не найдена в базе данных'
        else:
            detail = 'Категория не найдена в базе данных'
        super().__init__(detail=detail)


class CategorySlugAlreadyExistsException(BaseDatabaseException):
    def __init__(self, slug: str) -> None:
        detail = f'Категория со slug "{slug}" уже существует в базе данных. Slug должен быть уникальным'
        super().__init__(detail=detail)


class LocationNotFoundException(BaseDatabaseException):
    def __init__(self, location_id: int | None = None) -> None:
        if location_id is not None:
            detail = f'Местоположение с идентификатором {location_id} не найдено в базе данных'
        else:
            detail = 'Местоположение не найдено в базе данных'
        super().__init__(detail=detail)


class PostNotFoundException(BaseDatabaseException):
    def __init__(self, post_id: int | None = None) -> None:
        if post_id is not None:
            detail = f'Публикация с идентификатором {post_id} не найдена в базе данных'
        else:
            detail = 'Публикация не найдена в базе данных'
        super().__init__(detail=detail)


class CommentNotFoundException(BaseDatabaseException):
    def __init__(self, comment_id: int | None = None) -> None:
        if comment_id is not None:
            detail = f'Комментарий с идентификатором {comment_id} не найден в базе данных'
        else:
            detail = 'Комментарий не найден в базе данных'
        super().__init__(detail=detail)


class DatabaseConnectionError(BaseDatabaseException):
    def __init__(self, original_error: str | None = None) -> None:
        detail = 'Ошибка подключения к базе данных'
        if original_error:
            detail += f'. Оригинальная ошибка: {original_error}'
        super().__init__(detail=detail)


class DatabaseIntegrityError(BaseDatabaseException):
    def __init__(self, entity: str = 'запись', constraint_type: str | None = None, original_error: str | None = None) -> None:
        detail = f'Нарушение целостности базы данных при операции с сущностью "{entity}"'
        if constraint_type:
            detail += f'. Тип ограничения: {constraint_type}'
        if original_error:
            detail += f'. Детали: {original_error}'
        super().__init__(detail=detail)


class DatabaseOperationalError(BaseDatabaseException):
    def __init__(self, operation: str = 'операция', original_error: str | None = None) -> None:
        detail = f'Ошибка выполнения операции "{operation}" в базе данных'
        if original_error:
            detail += f'. Детали: {original_error}'
        super().__init__(detail=detail)


class DatabaseTimeoutError(BaseDatabaseException):
    def __init__(self, operation: str = 'операция', timeout_seconds: int | None = None) -> None:
        detail = f'Превышено время ожидания выполнения операции "{operation}" в базе данных'
        if timeout_seconds is not None:
            detail += f'. Таймаут: {timeout_seconds} секунд'
        super().__init__(detail=detail)


def handle_database_exception(exc: SQLAlchemyError, entity: str = 'запись') -> BaseDatabaseException:
    error_message = str(exc)
    orig_error = str(exc.orig) if hasattr(exc, 'orig') else None
    
    if isinstance(exc, IntegrityError):
        if 'username' in orig_error.lower():
            return UserUsernameAlreadyExistsException(username='неизвестно')
        if 'email' in orig_error.lower():
            return UserEmailAlreadyExistsException(email='неизвестно')
        if 'slug' in orig_error.lower():
            return CategorySlugAlreadyExistsException(slug='неизвестно')
        return DatabaseIntegrityError(
            entity=entity,
            constraint_type='уникальность или внешний ключ',
            original_error=error_message
        )
    
    if isinstance(exc, OperationalError):
        if 'timeout' in orig_error.lower() or 'locked' in orig_error.lower():
            return DatabaseTimeoutError(operation=f'работа с {entity}')
        return DatabaseConnectionError(original_error=error_message)
    
    return DatabaseOperationalError(
        operation=f'работа с {entity}',
        original_error=error_message
    )
