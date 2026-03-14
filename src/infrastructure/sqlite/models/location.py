from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlite.metadata import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlite.models.post import Post


class Location(Base):
    __tablename__ = 'blog_location'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    name: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[list['Post']] = relationship(
        'Post', back_populates='location', foreign_keys='Post.location_id'
    )
