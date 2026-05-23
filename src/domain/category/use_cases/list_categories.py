from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.category import CategoryRepository
from src.schemas.categories import CategoryResponseSchema


class GetCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> list[CategoryResponseSchema]:
        async with self._database.session() as session:
            categories = await self._repo.get_all(session=session)
            return [
                CategoryResponseSchema.model_validate(obj=cat)
                for cat in categories
            ]
