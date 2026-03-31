from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            category = self._repo.get(session=session, category_id=category_id)
            self._repo.delete(session=session, category=category)
