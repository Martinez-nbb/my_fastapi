from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.metadata import Base


class Comment(Base):
    __tablename__ = 'blog_comment'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)
    post_id: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(nullable=False)
