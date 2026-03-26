from pydantic import EmailStr


class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с идентификатором {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с именем {username} не найден"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )
        super().__init__(detail=self._exception_text_template)


class UserUsernameOrEmailIsNotUniqueException(BaseDomainException):
    def __init__(self, detail: str) -> None:
        self._exception_text_template = detail
        super().__init__(detail=self._exception_text_template)

    @classmethod
    def from_username(
        cls, username: str
    ) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = f"Пользователь с именем {username} уже существует"
        return cls(detail=detail)

    @classmethod
    def from_email(
        cls, email: str
    ) -> 'UserUsernameOrEmailIsNotUniqueException':
        detail = f"Пользователь с email {email} уже существует"
        return cls(detail=detail)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с идентификатором {id} не найдена"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Местоположение с идентификатором {id} не найдено"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Публикация с идентификатором {id} не найдена"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с идентификатором {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)
