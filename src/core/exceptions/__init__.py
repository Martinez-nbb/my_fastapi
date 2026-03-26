from src.core.exceptions.database_exceptions import (
    BaseDatabaseException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    CommentNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    BaseDomainException,
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserUsernameOrEmailIsNotUniqueException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
    CommentNotFoundByIdException,
)

__all__ = [
    # Database exceptions
    'BaseDatabaseException',
    'UserNotFoundException',
    'UserUsernameAlreadyExistsException',
    'UserEmailAlreadyExistsException',
    'CategoryNotFoundException',
    'LocationNotFoundException',
    'PostNotFoundException',
    'CommentNotFoundException',
    # Domain exceptions
    'BaseDomainException',
    'UserNotFoundByIdException',
    'UserNotFoundByUsernameException',
    'UserUsernameOrEmailIsNotUniqueException',
    'CategoryNotFoundByIdException',
    'LocationNotFoundByIdException',
    'PostNotFoundByIdException',
    'CommentNotFoundByIdException',
]
