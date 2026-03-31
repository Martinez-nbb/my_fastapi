"""
Исключения уровня домена.

Эти исключения используются use case для сигнализации о бизнес-ошибках.
Они транслируются в HTTPException на уровне API router.
"""


class BaseDomainException(Exception):
    """Базовое исключение для ошибок домена."""

    def __init__(self, detail: str) -> None:
        self._detail = detail
        self.error_type = self.__class__.__name__

    def get_detail(self) -> str:
        return self._detail

    def to_dict(self) -> dict:
        return {
            'error_type': self.error_type,
            'detail': self._detail,
        }


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с идентификатором {id} не найден в системе"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.user_id = id


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с именем '{username}' не найден в системе"

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(username=username)
        super().__init__(detail=detail)
        self.username = username


class UserNotFoundByEmailException(BaseDomainException):
    _exception_text_template = "Пользователь с email '{email}' не найден в системе"

    def __init__(self, email: str) -> None:
        detail = self._exception_text_template.format(email=email)
        super().__init__(detail=detail)
        self.email = email


class UserUsernameOrEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template_username = "Пользователь с именем '{username}' уже существует"
    _exception_text_template_email = "Пользователь с email '{email}' уже существует"

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail)

    @classmethod
    def from_username(cls, username: str) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = cls._exception_text_template_username.format(username=username)
        return cls(detail=detail)

    @classmethod
    def from_email(cls, email: str) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = cls._exception_text_template_email.format(email=email)
        return cls(detail=detail)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с идентификатором {id} не найдена в системе"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.category_id = id


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория со slug '{slug}' не найдена в системе"

    def __init__(self, slug: str) -> None:
        detail = self._exception_text_template.format(slug=slug)
        super().__init__(detail=detail)
        self.slug = slug


class CategorySlugAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Категория со slug '{slug}' уже существует"

    def __init__(self, slug: str) -> None:
        detail = self._exception_text_template.format(slug=slug)
        super().__init__(detail=detail)
        self.slug = slug


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Местоположение с идентификатором {id} не найдено в системе"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.location_id = id


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Публикация с идентификатором {id} не найдена в системе"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.post_id = id


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с идентификатором {id} не найден в системе"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.comment_id = id


class AuthorNotFoundException(BaseDomainException):
    _exception_text_template = "Автор с идентификатором {author_id} не найден в системе"

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(author_id=author_id)
        super().__init__(detail=detail)
        self.author_id = author_id
