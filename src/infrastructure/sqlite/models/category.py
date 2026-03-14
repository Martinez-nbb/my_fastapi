from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlite.database import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlite.models.post import Post


class Category(Base):
    __tablename__ = 'blog_category'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)

    posts: Mapped[list['Post']] = relationship(
        'Post', back_populates='category', foreign_keys='Post.category_id'
    )
