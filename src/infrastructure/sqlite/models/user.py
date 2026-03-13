from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.metadata import Base


class User(Base):
    __tablename__ = 'auth_user'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    password: Mapped[str] = mapped_column(nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False, default='')
    last_name: Mapped[str] = mapped_column(nullable=False, default='')
    email: Mapped[str] = mapped_column(nullable=False, default='')
    is_staff: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    date_joined: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
