from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import CategoryResponseSchema


class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.get(session=session, category_id=category_id)
            return CategoryResponseSchema.model_validate(obj=category)
