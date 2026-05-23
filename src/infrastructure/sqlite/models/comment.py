from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlite.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlite.models.post import Post
    from src.infrastructure.sqlite.models.user import User
    from src.infrastructure.sqlite.models.comment_image import CommentImage


class Comment(Base):
    __tablename__ = 'blog_comment'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey('blog_post.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey('auth_user.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )

    post: Mapped['Post'] = relationship(
        'Post', back_populates='comments', foreign_keys=[post_id]
    )
    author: Mapped['User'] = relationship(
        'User', back_populates='comments', foreign_keys=[author_id]
    )
    images: Mapped[list['CommentImage']] = relationship(
        'CommentImage',
        back_populates='comment',
        foreign_keys='CommentImage.comment_id',
        cascade='all, delete-orphan',
    )
