from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.postgres.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.postgres.models.comment import Comment


class CommentImage(Base):
    __tablename__ = 'blog_comment_image'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    comment_id: Mapped[int] = mapped_column(
        ForeignKey('blog_comment.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(nullable=False)
    original_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    comment: Mapped['Comment'] = relationship(
        'Comment', back_populates='images', foreign_keys=[comment_id]
    )
