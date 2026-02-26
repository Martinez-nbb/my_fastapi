from fastapi import APIRouter, status, HTTPException

from typing import List

from datetime import datetime

from src.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentResponseSchema,
)

from src.schemas.users import UserSchema
router = APIRouter(
    # prefix="/comments"  # Добавляется при подключении в app.py
    # tags=["Comments"]   # Добавляется при подключении в app.py
)
# Список для хранения данных о комментариях
comments_db: List[dict] = []

# Счётчик для генерации уникальных ID комментариев
_comments_counter = 0

TEST_AUTHOR = UserSchema(
    username="commenter",
    password="secret123",
    email="commenter@example.com",
)
def _get_comment_with_relations(comment_data: dict) -> dict:
    
    comment_data["author"] = TEST_AUTHOR
    
    comment_data.pop("author_id", None)
    
    return comment_data

@router.get(
    "/list",
    response_model=List[CommentResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех комментариев",
    description="Возвращает список всех комментариев",
)
async def get_comments_list() -> List[dict]:
    
    # Добавляем вложенные объекты ко всем комментариям
    return [_get_comment_with_relations(c.copy()) for c in comments_db]
@router.get(
    "/list/by_post/{post_id}",
    response_model=List[CommentResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить комментарии к публикации",
    description="Возвращает все комментарии к конкретной публикации, отсортированные по дате создания",
)
async def get_comments_by_post(post_id: int) -> List[dict]:
    
    post_comments = [
        _get_comment_with_relations(c.copy())
        for c in comments_db
        if c["post_id"] == post_id
    ]
    post_comments.sort(key=lambda x: x.get("created_at", datetime.min))
    
    return post_comments
@router.get(
    "/get/{comment_id}",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить комментарий по ID",
    description="Возвращает комментарий по уникальному идентификатору",
)
async def get_comment(comment_id: int) -> dict:
    
    for comment in comments_db:
        if comment["id"] == comment_id:
            return _get_comment_with_relations(comment.copy())
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Комментарий с id={comment_id} не найден",
    )
@router.post(
    "/create",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый комментарий",
    description="Создаёт новый комментарий к публикации",
)
async def create_comment(comment: CommentCreateSchema) -> dict:
    
    global _comments_counter
    
    from src.api.posts import posts_db
    
    post_exists = any(p["id"] == comment.post_id for p in posts_db)
    
    if not post_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с id={comment.post_id} не найдена",
        )
    _comments_counter += 1
    new_id = _comments_counter
    comment_data = comment.model_dump()
    
    comment_data["id"] = new_id
    comment_data["created_at"] = datetime.now()
    comment_data = _get_comment_with_relations(comment_data)
    comments_db.append(comment_data)
    return comment_data
@router.put(
    "/update/{comment_id}",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить комментарий",
    description="Обновляет существующий комментарий (partial update)",
)
async def update_comment(comment_id: int, comment: CommentUpdateSchema) -> dict:
    
    for idx, c in enumerate(comments_db):
        if c["id"] == comment_id:
            update_data = comment.model_dump(exclude_unset=True)
            comments_db[idx].update(update_data)
            return _get_comment_with_relations(comments_db[idx].copy())
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Комментарий с id={comment_id} не найден",
    )
@router.delete(
    "/delete/{comment_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить комментарий",
    description="Удаляет комментарий по уникальному идентификатору",
)
async def delete_comment(comment_id: int) -> dict:
    
    for idx, c in enumerate(comments_db):
        if c["id"] == comment_id:
            # Найден — удаляем
            comments_db.pop(idx)
            return {"message": "Комментарий успешно удален"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Комментарий с id={comment_id} не найден",
    )
