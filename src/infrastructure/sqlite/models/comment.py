from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlite.database import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlite.models.post import Post
    from src.infrastructure.sqlite.models.user import User


class Comment(Base):
    __tablename__ = 'blog_comment'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey('blog_post.id', ondelete='CASCADE'), nullable=False
    )
    text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey('auth_user.id', ondelete='CASCADE'), nullable=False
    )

    post: Mapped['Post'] = relationship(
        'Post', back_populates='comments', foreign_keys=[post_id]
    )
    author: Mapped['User'] = relationship(
        'User', back_populates='comments', foreign_keys=[author_id]
    )
