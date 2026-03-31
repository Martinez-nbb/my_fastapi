from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        with self._database.session() as session:
            user = self._repo.get(
                session=session,
                user_id=user_id,
            )

            self._repo.delete(session=session, user=user)
