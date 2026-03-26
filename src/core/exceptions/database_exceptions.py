from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError, DBAPIError


class BaseDatabaseException(Exception):
    def __init__(
        self,
        detail: str | None = None,
        original_error: str | None = None,
        sql_query: str | None = None,
        params: dict | None = None,
    ) -> None:
        self._detail = detail
        self._original_error = original_error
        self._sql_query = sql_query
        self._params = params
        self.error_type = self.__class__.__name__

    def get_detail(self) -> str:
        return self._detail

    def get_original_error(self) -> str | None:
        return self._original_error

    def to_dict(self) -> dict:
        result = {
            'error_type': self.error_type,
            'detail': self._detail,
        }
        if self._original_error:
            result['original_error'] = self._original_error
        return result


class UserNotFoundException(BaseDatabaseException):
    def __init__(
        self,
        user_id: int | None = None,
        username: str | None = None,
        original_error: str | None = None,
    ) -> None:
        if user_id is not None:
            detail = f'Пользователь с идентификатором {user_id} не найден в базе данных'
        elif username is not None:
            detail = f'Пользователь с именем "{username}" не найден в базе данных'
        else:
            detail = 'Пользователь не найден в базе данных'
        super().__init__(detail=detail, original_error=original_error)


class UserUsernameAlreadyExistsException(BaseDatabaseException):
    def __init__(self, username: str, original_error: str | None = None) -> None:
        detail = (
            f'Пользователь с именем "{username}" уже существует в базе данных. '
            f'Выберите другое имя для регистрации'
        )
        super().__init__(detail=detail, original_error=original_error)


class UserEmailAlreadyExistsException(BaseDatabaseException):
    def __init__(self, email: str, original_error: str | None = None) -> None:
        detail = (
            f'Пользователь с email "{email}" уже существует в базе данных. '
            f'Используйте другой email или войдите в существующий аккаунт'
        )
        super().__init__(detail=detail, original_error=original_error)


class CategoryNotFoundException(BaseDatabaseException):
    def __init__(
        self,
        category_id: int | None = None,
        slug: str | None = None,
        original_error: str | None = None,
    ) -> None:
        if category_id is not None:
            detail = f'Категория с идентификатором {category_id} не найдена в базе данных'
        elif slug is not None:
            detail = f'Категория со slug "{slug}" не найдена в базе данных'
        else:
            detail = 'Категория не найдена в базе данных'
        super().__init__(detail=detail, original_error=original_error)


class CategorySlugAlreadyExistsException(BaseDatabaseException):
    def __init__(self, slug: str, original_error: str | None = None) -> None:
        detail = (
            f'Категория со slug "{slug}" уже существует в базе данных. '
            f'Slug должен быть уникальным для каждой категории'
        )
        super().__init__(detail=detail, original_error=original_error)


class LocationNotFoundException(BaseDatabaseException):
    def __init__(
        self,
        location_id: int | None = None,
        original_error: str | None = None,
    ) -> None:
        if location_id is not None:
            detail = f'Местоположение с идентификатором {location_id} не найдено в базе данных'
        else:
            detail = 'Местоположение не найдено в базе данных'
        super().__init__(detail=detail, original_error=original_error)


class PostNotFoundException(BaseDatabaseException):
    def __init__(
        self,
        post_id: int | None = None,
        original_error: str | None = None,
    ) -> None:
        if post_id is not None:
            detail = f'Публикация с идентификатором {post_id} не найдена в базе данных'
        else:
            detail = 'Публикация не найдена в базе данных'
        super().__init__(detail=detail, original_error=original_error)


class CommentNotFoundException(BaseDatabaseException):
    def __init__(
        self,
        comment_id: int | None = None,
        original_error: str | None = None,
    ) -> None:
        if comment_id is not None:
            detail = f'Комментарий с идентификатором {comment_id} не найден в базе данных'
        else:
            detail = 'Комментарий не найден в базе данных'
        super().__init__(detail=detail, original_error=original_error)


class DatabaseConnectionError(BaseDatabaseException):
    def __init__(
        self,
        original_error: str | None = None,
        connection_url: str | None = None,
    ) -> None:
        detail = 'Ошибка подключения к базе данных'
        if connection_url:
            detail += f' по адресу {connection_url}'
        if original_error:
            detail += f'. Оригинальная ошибка: {original_error}'
        super().__init__(detail=detail, original_error=original_error)


class DatabaseIntegrityError(BaseDatabaseException):
    def __init__(
        self,
        entity: str = 'запись',
        constraint_type: str | None = None,
        constraint_name: str | None = None,
        original_error: str | None = None,
        sql_query: str | None = None,
    ) -> None:
        detail = f'Нарушение целостности базы данных при операции с сущностью "{entity}"'
        if constraint_type:
            detail += f'. Тип ограничения: {constraint_type}'
        if constraint_name:
            detail += f'. Имя ограничения: {constraint_name}'
        super().__init__(
            detail=detail,
            original_error=original_error,
            sql_query=sql_query,
        )


class DatabaseForeignKeyError(DatabaseIntegrityError):
    def __init__(
        self,
        entity: str = 'запись',
        referenced_table: str | None = None,
        original_error: str | None = None,
    ) -> None:
        detail = f'Нарушение внешнего ключа при операции с сущностью "{entity}"'
        if referenced_table:
            detail += f'. Таблица ссылки: {referenced_table}'
        detail += '. Убедитесь, что связанные записи существуют'
        super().__init__(
            entity=entity,
            constraint_type='FOREIGN KEY',
            original_error=original_error,
        )


class DatabaseUniqueConstraintError(DatabaseIntegrityError):
    def __init__(
        self,
        entity: str = 'запись',
        field_name: str | None = None,
        value: str | None = None,
        original_error: str | None = None,
    ) -> None:
        detail = f'Нарушение уникальности при операции с сущностью "{entity}"'
        if field_name and value:
            detail += f'. Поле "{field_name}" со значением "{value}" уже существует'
        detail += '. Значение должно быть уникальным'
        super().__init__(
            entity=entity,
            constraint_type='UNIQUE',
            original_error=original_error,
        )


class DatabaseNotNullConstraintError(DatabaseIntegrityError):
    def __init__(
        self,
        entity: str = 'запись',
        field_name: str | None = None,
        original_error: str | None = None,
    ) -> None:
        detail = f'Нарушение ограничения NOT NULL при операции с сущностью "{entity}"'
        if field_name:
            detail += f'. Поле "{field_name}" не может быть пустым'
        super().__init__(
            entity=entity,
            constraint_type='NOT NULL',
            original_error=original_error,
        )


class DatabaseCheckConstraintError(DatabaseIntegrityError):
    def __init__(
        self,
        entity: str = 'запись',
        constraint_name: str | None = None,
        original_error: str | None = None,
    ) -> None:
        detail = f'Нарушение проверочного ограничения при операции с сущностью "{entity}"'
        if constraint_name:
            detail += f'. Имя ограничения: {constraint_name}'
        super().__init__(
            entity=entity,
            constraint_type='CHECK',
            constraint_name=constraint_name,
            original_error=original_error,
        )


class DatabaseOperationalError(BaseDatabaseException):
    def __init__(
        self,
        operation: str = 'операция',
        original_error: str | None = None,
        sql_query: str | None = None,
    ) -> None:
        detail = f'Ошибка выполнения операции "{operation}" в базе данных'
        if original_error:
            detail += f'. Детали: {original_error}'
        super().__init__(
            detail=detail,
            original_error=original_error,
            sql_query=sql_query,
        )


class DatabaseTimeoutError(DatabaseOperationalError):
    def __init__(
        self,
        operation: str = 'операция',
        timeout_seconds: int | None = None,
        original_error: str | None = None,
    ) -> None:
        detail = f'Превышено время ожидания выполнения операции "{operation}" в базе данных'
        if timeout_seconds is not None:
            detail += f'. Таймаут: {timeout_seconds} секунд'
        detail += '. Попробуйте повторить операцию позже или оптимизировать запрос'
        super().__init__(
            operation=operation,
            original_error=original_error,
        )


class DatabaseLockError(DatabaseOperationalError):
    def __init__(
        self,
        operation: str = 'операция',
        locked_table: str | None = None,
        original_error: str | None = None,
    ) -> None:
        detail = f'Ошибка блокировки при выполнении операции "{operation}" в базе данных'
        if locked_table:
            detail += f'. Заблокированная таблица: {locked_table}'
        detail += '. Другая транзакция удерживает блокировку. Попробуйте повторить операцию'
        super().__init__(
            operation=operation,
            original_error=original_error,
        )


class DatabaseSyntaxError(BaseDatabaseException):
    def __init__(
        self,
        original_error: str | None = None,
        sql_query: str | None = None,
    ) -> None:
        detail = 'Ошибка синтаксиса SQL запроса'
        if sql_query:
            detail += f'. Запрос: {sql_query[:200]}...'
        if original_error:
            detail += f'. Детали: {original_error}'
        super().__init__(
            detail=detail,
            original_error=original_error,
            sql_query=sql_query,
        )


def handle_database_exception(
    exc: SQLAlchemyError,
    entity: str = 'запись',
    sql_query: str | None = None,
    params: dict | None = None,
) -> BaseDatabaseException:
    error_message = str(exc)
    orig_error = str(exc.orig) if hasattr(exc, 'orig') else None
    
    if isinstance(exc, IntegrityError):
        orig_lower = orig_error.lower() if orig_error else ''
        
        if 'username' in orig_lower:
            return UserUsernameAlreadyExistsException(
                username='неизвестно',
                original_error=error_message,
            )
        if 'email' in orig_lower:
            return UserEmailAlreadyExistsException(
                email='неизвестно',
                original_error=error_message,
            )
        if 'slug' in orig_lower:
            return CategorySlugAlreadyExistsException(
                slug='неизвестно',
                original_error=error_message,
            )
        
        if 'foreign key' in orig_lower:
            return DatabaseForeignKeyError(
                entity=entity,
                original_error=error_message,
            )
        
        if 'unique' in orig_lower or 'duplicate' in orig_lower:
            field_name = _extract_field_name(orig_lower)
            return DatabaseUniqueConstraintError(
                entity=entity,
                field_name=field_name,
                original_error=error_message,
            )
        
        if 'not null' in orig_lower:
            field_name = _extract_field_name(orig_lower)
            return DatabaseNotNullConstraintError(
                entity=entity,
                field_name=field_name,
                original_error=error_message,
            )
        
        if 'check' in orig_lower:
            return DatabaseCheckConstraintError(
                entity=entity,
                original_error=error_message,
            )
        
        return DatabaseIntegrityError(
            entity=entity,
            constraint_type='неизвестный тип',
            original_error=error_message,
            sql_query=sql_query,
        )
    
    if isinstance(exc, OperationalError):
        orig_lower = orig_error.lower() if orig_error else ''
        
        if 'timeout' in orig_lower or 'timed out' in orig_lower:
            return DatabaseTimeoutError(
                operation=f'работа с {entity}',
                original_error=error_message,
            )
        
        if 'locked' in orig_lower or 'deadlock' in orig_lower:
            return DatabaseLockError(
                operation=f'работа с {entity}',
                original_error=error_message,
            )
        
        if 'no such table' in orig_lower or 'doesn\'t exist' in orig_lower:
            return DatabaseOperationalError(
                operation=f'работа с {entity}',
                original_error=error_message,
                sql_query=sql_query,
            )
        
        return DatabaseConnectionError(
            original_error=error_message,
        )
    
    if isinstance(exc, DBAPIError):
        return DatabaseOperationalError(
            operation=f'работа с {entity}',
            original_error=error_message,
            sql_query=sql_query,
        )
    
    return BaseDatabaseException(
        detail=f'Неизвестная ошибка базы данных при работе с сущностью {entity}',
        original_error=error_message,
    )


def _extract_field_name(error_string: str) -> str | None:
    import re
    match = re.search(r'column[s]?[:\s]+([a-zA-Z_][a-zA-Z0-9_]*)', error_string)
    if match:
        return match.group(1)
    match = re.search(r'[\'"]([a-zA-Z_][a-zA-Z0-9_]*)[\'"]', error_string)
    if match:
        return match.group(1)
    return None
