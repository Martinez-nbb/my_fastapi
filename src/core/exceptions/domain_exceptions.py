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
    def __init__(self, id: int) -> None:
        detail = (
            f'Пользователь с идентификатором {id} не найден в системе. '
            f'Проверьте корректность переданного идентификатора пользователя'
        )
        super().__init__(detail=detail)
        self.user_id = id


class UserNotFoundByUsernameException(BaseDomainException):
    def __init__(self, username: str) -> None:
        detail = (
            f'Пользователь с именем "{username}" не найден в системе. '
            f'Проверьте корректность переданного имени пользователя'
        )
        super().__init__(detail=detail)
        self.username = username


class UserNotFoundByEmailException(BaseDomainException):
    def __init__(self, email: str) -> None:
        detail = (
            f'Пользователь с email "{email}" не найден в системе. '
            f'Проверьте корректность переданного email'
        )
        super().__init__(detail=detail)
        self.email = email


class UserUsernameOrEmailIsNotUniqueException(BaseDomainException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail)

    @classmethod
    def from_username(cls, username: str) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = (
            f'Пользователь с именем "{username}" уже существует в системе. '
            f'Пожалуйста, выберите другое имя для регистрации'
        )
        return cls(detail=detail)

    @classmethod
    def from_email(cls, email: str) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = (
            f'Пользователь с email "{email}" уже существует в системе. '
            f'Пожалуйста, используйте другой email или войдите в существующий аккаунт'
        )
        return cls(detail=detail)


class CategoryNotFoundByIdException(BaseDomainException):
    def __init__(self, id: int) -> None:
        detail = (
            f'Категория с идентификатором {id} не найдена в системе. '
            f'Проверьте корректность переданного идентификатора категории'
        )
        super().__init__(detail=detail)
        self.category_id = id


class CategoryNotFoundBySlugException(BaseDomainException):
    def __init__(self, slug: str) -> None:
        detail = (
            f'Категория со slug "{slug}" не найдена в системе. '
            f'Проверьте корректность переданного slug категории'
        )
        super().__init__(detail=detail)
        self.slug = slug


class CategorySlugAlreadyExistsException(BaseDomainException):
    def __init__(self, slug: str) -> None:
        detail = (
            f'Категория со slug "{slug}" уже существует в системе. '
            f'Slug должен быть уникальным для каждой категории'
        )
        super().__init__(detail=detail)
        self.slug = slug


class LocationNotFoundByIdException(BaseDomainException):
    def __init__(self, id: int) -> None:
        detail = (
            f'Местоположение с идентификатором {id} не найдено в системе. '
            f'Проверьте корректность переданного идентификатора местоположения'
        )
        super().__init__(detail=detail)
        self.location_id = id


class PostNotFoundByIdException(BaseDomainException):
    def __init__(self, id: int) -> None:
        detail = (
            f'Публикация с идентификатором {id} не найдена в системе. '
            f'Возможно, публикация была удалена или имеет другой идентификатор'
        )
        super().__init__(detail=detail)
        self.post_id = id


class PostNotFoundException(BaseDomainException):
    def __init__(self, post_id: int, reason: str | None = None) -> None:
        detail = f'Публикация с идентификатором {post_id} не найдена'
        if reason:
            detail += f'. Причина: {reason}'
        super().__init__(detail=detail)
        self.post_id = post_id


class CommentNotFoundByIdException(BaseDomainException):
    def __init__(self, id: int) -> None:
        detail = (
            f'Комментарий с идентификатором {id} не найден в системе. '
            f'Возможно, комментарий был удалён или имеет другой идентификатор'
        )
        super().__init__(detail=detail)
        self.comment_id = id


class AuthorNotFoundException(BaseDomainException):
    def __init__(self, author_id: int) -> None:
        detail = (
            f'Автор с идентификатором {author_id} не найден в системе. '
            f'Невозможно создать публикацию без существующего автора'
        )
        super().__init__(detail=detail)
        self.author_id = author_id
