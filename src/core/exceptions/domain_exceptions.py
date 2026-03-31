from pydantic import EmailStr


class BaseDomainException(Exception):
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
    _exception_text_template = "Пользователь с id '{id}' не найден"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.user_id = id


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с логином '{username}' не найден"

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(username=username)
        super().__init__(detail=detail)
        self.username = username


class UserNotFoundByEmailException(BaseDomainException):
    _exception_text_template = "Пользователь с email '{email}' не найден"

    def __init__(self, email: str) -> None:
        detail = self._exception_text_template.format(email=email)
        super().__init__(detail=detail)
        self.email = email


class UserUsernameOrEmailIsNotUniqueException(BaseDomainException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail)

    @classmethod
    def from_username(cls, username: str) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = f"Пользователь с логином '{username}' уже существует"
        return cls(detail=detail)

    @classmethod
    def from_email(cls, email: EmailStr) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = f"Пользователь с email '{email}' уже существует"
        return cls(detail=detail)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с id '{id}' не найдена"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.category_id = id


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория со slug '{slug}' не найдена"

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
    _exception_text_template = "Местоположение с id '{id}' не найдено"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.location_id = id


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Публикация с id '{id}' не найдена"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.post_id = id


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с id '{id}' не найден"

    def __init__(self, id: int) -> None:
        detail = self._exception_text_template.format(id=id)
        super().__init__(detail=detail)
        self.comment_id = id


class AuthorNotFoundException(BaseDomainException):
    _exception_text_template = "Автор с id '{author_id}' не найден"

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(author_id=author_id)
        super().__init__(detail=detail)
        self.author_id = author_id
