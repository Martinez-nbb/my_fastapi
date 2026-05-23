class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        message = detail or "Database error occurred"
        self._detail = detail
        super().__init__(message)


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


class AuthorNotFoundException(BaseDatabaseException):
    pass


class PostImageNotFoundException(BaseDatabaseException):
    def __init__(self, image_id: int | None = None) -> None:
        detail = f"Изображение поста с id '{image_id}' не найдено" if image_id else "Изображение поста не найдено"
        super().__init__(detail=detail)


class CommentImageNotFoundException(BaseDatabaseException):
    def __init__(self, image_id: int | None = None) -> None:
        detail = f"Изображение комментария с id '{image_id}' не найдено" if image_id else "Изображение комментария не найдено"
        super().__init__(detail=detail)
