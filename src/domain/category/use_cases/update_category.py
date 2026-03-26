from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import CategoryUpdateSchema, CategoryResponseSchema


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        category_id: int,
        data: CategoryUpdateSchema,
    ) -> CategoryResponseSchema:
        with self._database.session() as session:
            try:
                category = self._repo.get(
                    session=session,
                    category_id=category_id,
                )
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=category_id)

            self._repo.update(
                session=session,
                category=category,
                data=data,
            )

            return CategoryResponseSchema.model_validate(obj=category)
