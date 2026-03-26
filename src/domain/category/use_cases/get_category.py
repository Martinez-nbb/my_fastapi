from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import CategoryResponseSchema


class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        with self._database.session() as session:
            try:
                category = self._repo.get(
                    session=session,
                    category_id=category_id,
                )
            except CategoryNotFoundException as exc:
                raise CategoryNotFoundByIdException(id=category_id)

            return CategoryResponseSchema.model_validate(obj=category)
