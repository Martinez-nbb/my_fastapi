from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.sqlite.database import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlite.models.user import User
    from src.infrastructure.sqlite.models.category import Category
    from src.infrastructure.sqlite.models.location import Location
    from src.infrastructure.sqlite.models.comment import Comment


class Post(Base):
    __tablename__ = 'blog_post'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey('auth_user.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    location_id: Mapped[int | None] = mapped_column(
        ForeignKey('blog_location.id', ondelete='SET NULL'),
        index=True,
        nullable=True,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey('blog_category.id', ondelete='SET NULL'),
        index=True,
        nullable=True,
    )
    image: Mapped[str] = mapped_column(nullable=False, default='')

    author: Mapped['User'] = relationship(
        'User', back_populates='posts', foreign_keys=[author_id]
    )
    location: Mapped['Location | None'] = relationship(
        'Location', back_populates='posts', foreign_keys=[location_id]
    )
    category: Mapped['Category | None'] = relationship(
        'Category', back_populates='posts', foreign_keys=[category_id]
    )
    comments: Mapped[list['Comment']] = relationship(
        'Comment', back_populates='post', foreign_keys='Comment.post_id'
    )
