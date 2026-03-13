from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.metadata import Base


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
    author_id: Mapped[int] = mapped_column(nullable=False)
    location_id: Mapped[int | None] = mapped_column(nullable=True)
    category_id: Mapped[int | None] = mapped_column(nullable=True)
    image: Mapped[str | None] = mapped_column(nullable=True)
