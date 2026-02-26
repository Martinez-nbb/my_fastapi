
from fastapi import APIRouter, status, HTTPException

from typing import List

from datetime import datetime

from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)

from src.schemas.users import UserSchema
router = APIRouter(
    # prefix="/posts"  # Добавляется при подключении в app.py
    # tags=["Posts"]   # Добавляется при подключении в app.py
)
posts_db: List[dict] = []

_posts_counter = 0
TEST_AUTHOR = UserSchema(
    username="test_author",
    password="secret123",
    email="author@example.com",
)
def _get_post_with_relations(post_data: dict) -> dict:
    
    post_data["author"] = TEST_AUTHOR
    # Импортируем хранилище местоположений
    # Импортируем здесь, чтобы избежать циклического импорта
    from src.api.locations import locations_db
    
    location_id = post_data.get("location_id")
    
    if location_id is not None:
        location_found = None
        for loc in locations_db:
            if loc["id"] == location_id:
                location_found = loc
                break
        
        post_data["location"] = location_found
    else:
        post_data["location"] = None
    
    from src.api.categories import categories_db
    
    category_id = post_data.get("category_id")
    
    if category_id is not None:
        category_found = None
        for cat in categories_db:
            if cat["id"] == category_id:
                category_found = cat
                break
        post_data["category"] = category_found
    else:
        post_data["category"] = None
    
    post_data.pop("location_id", None)
    post_data.pop("category_id", None)
    post_data.pop("author_id", None)
    
    return post_data
@router.get(
    "/list",
    response_model=List[PostResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех публикаций",
    description="Возвращает список всех публикаций с вложенными объектами (author, location, category)",
)
async def get_posts_list() -> List[dict]:
    
    return [_get_post_with_relations(post.copy()) for post in posts_db]

@router.get(
    "/get/{post_id}",
    response_model=PostResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить публикацию по ID",
    description="Возвращает публикацию по уникальному идентификатору с вложенными объектами",
)
async def get_post(post_id: int) -> dict:
    
    for post in posts_db:
        if post["id"] == post_id:
            return _get_post_with_relations(post.copy())
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Публикация с id={post_id} не найдена",
    )
@router.post(
    "/create",
    response_model=PostResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую публикацию",
    description="Создаёт новую публикацию с указанными данными",
)
async def create_post(post: PostCreateSchema) -> dict:
    
    global _posts_counter
    _posts_counter += 1
    new_id = _posts_counter
    
    post_data = post.model_dump()
    
    post_data["id"] = new_id
    
    post_data["created_at"] = datetime.now()
    post_data["image"] = None
    post_data = _get_post_with_relations(post_data)
    posts_db.append(post_data)
    return post_data
@router.put(
    "/update/{post_id}",
    response_model=PostResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить публикацию",
    description="Обновляет существующую публикацию (partial update)",
)
async def update_post(post_id: int, post: PostUpdateSchema) -> dict:
    
    for idx, p in enumerate(posts_db):
        if p["id"] == post_id:
            
            update_data = post.model_dump(exclude_unset=True)
            posts_db[idx].update(update_data)
            return _get_post_with_relations(posts_db[idx].copy())
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Публикация с id={post_id} не найдена",
    )
@router.delete(
    "/delete/{post_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить публикацию",
    description="Удаляет публикацию по уникальному идентификатору",
)
async def delete_post(post_id: int) -> dict:
    
    for idx, p in enumerate(posts_db):
        if p["id"] == post_id:
            posts_db.pop(idx)
            return {"message": "Публикация успешно удалена"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Публикация с id={post_id} не найдена",
    )