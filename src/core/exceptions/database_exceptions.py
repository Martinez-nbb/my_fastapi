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


class LocationNotFoundException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class CommentNotFoundException(BaseDatabaseException):
    pass
