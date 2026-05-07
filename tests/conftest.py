import pytest

from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase

from tests.mocks import FakeDatabase, FakeRepo, FakeSession


@pytest.fixture
def fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def fake_database(fake_session: FakeSession) -> FakeDatabase:
    return FakeDatabase(fake_session)


@pytest.fixture
def fake_repo() -> FakeRepo:
    return FakeRepo()


@pytest.fixture
def authenticate_user_use_case(fake_database: FakeDatabase, fake_repo: FakeRepo) -> AuthenticateUserUseCase:
    uc: AuthenticateUserUseCase = AuthenticateUserUseCase()
    uc._database = fake_database
    uc._repo = fake_repo
    return uc


@pytest.fixture
def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


@pytest.fixture
def create_user_use_case(fake_database: FakeDatabase, fake_repo: FakeRepo) -> CreateUserUseCase:
    uc: CreateUserUseCase = CreateUserUseCase()
    uc._database = fake_database
    uc._repo = fake_repo
    return uc


@pytest.fixture
def get_user_use_case(fake_database: FakeDatabase, fake_repo: FakeRepo) -> GetUserUseCase:
    uc: GetUserUseCase = GetUserUseCase()
    uc._database = fake_database
    uc._repo = fake_repo
    return uc


@pytest.fixture
def get_users_use_case(fake_database: FakeDatabase, fake_repo: FakeRepo) -> GetUsersUseCase:
    uc: GetUsersUseCase = GetUsersUseCase()
    uc._database = fake_database
    uc._repo = fake_repo
    return uc


@pytest.fixture
def update_user_use_case(fake_database: FakeDatabase, fake_repo: FakeRepo) -> UpdateUserUseCase:
    uc: UpdateUserUseCase = UpdateUserUseCase()
    uc._database = fake_database
    uc._repo = fake_repo
    return uc