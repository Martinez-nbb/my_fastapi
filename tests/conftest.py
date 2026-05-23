import pytest
from unittest.mock import patch
import httpx

from fastapi.testclient import TestClient
from src.app import create_app

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


# --- Fixtures for Integration Tests ---

@pytest.fixture
def test_app():
    """Yields the FastAPI application."""
    return create_app()


@pytest.fixture
def valid_user_payload():
    """Returns a dict with valid user registration data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def valid_post_payload():
    """Returns a dict with valid post creation data."""
    return {
        "title": "Test Post",
        "content": "This is a test post content.",
        "category_id": 1,
        "location_id": 1,
    }


@pytest.fixture
def mock_database():
    """Mocks the database singleton for integration tests."""
    # Patch in the infrastructure module and all domain modules that import it
    targets = [
        "src.infrastructure.postgres.database.database",
        "src.domain.user.use_cases.create_user.database",
        "src.domain.user.use_cases.get_user.database",
        "src.domain.user.use_cases.get_users.database",
        "src.domain.user.use_cases.update_user.database",
        "src.domain.user.use_cases.delete_user.database",
        "src.domain.auth.use_cases.authenticate_user.database",
    ]
    
    patches = [patch(target) for target in targets]
    mocks = [p.start() for p in patches]
        
    yield mocks[0]
    
    for p in patches:
        p.stop()


@pytest.fixture
def mock_repo():
    """Mocks the repository for integration tests."""
    targets = [
        "src.domain.user.use_cases.create_user.UserRepository",
        "src.domain.user.use_cases.get_user.UserRepository",
        "src.domain.user.use_cases.get_users.UserRepository",
        "src.domain.user.use_cases.update_user.UserRepository",
        "src.domain.user.use_cases.delete_user.UserRepository",
        "src.domain.auth.use_cases.authenticate_user.UserRepository",
    ]
    
    patches = [patch(target) for target in targets]
    mocks = [p.start() for p in patches]
        
    # Return a dict for easy access
    yield {
        "user": mocks[0],
        "auth": mocks[5],
    }
    
    for p in patches:
        p.stop()


@pytest.fixture
def async_client(test_app, mock_database, mock_repo):
    """Yields an async test client with mocked database."""
    import asyncio
    transport = httpx.ASGITransport(app=test_app)
    client = httpx.AsyncClient(transport=transport, base_url="http://test")
    yield client
    asyncio.run(client.aclose())