from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.postgres.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.postgres.models.post import Post


class PostImage(Base):
    __tablename__ = 'blog_post_image'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey('blog_post.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(nullable=False)
    original_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    post: Mapped['Post'] = relationship(
        'Post', back_populates='images', foreign_keys=[post_id]
    )
