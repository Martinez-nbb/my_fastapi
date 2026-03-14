from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        db_path = base_dir / 'django_sprint4' / 'blogicum' / 'db.sqlite3'
        self._db_url = f'sqlite:///{db_path}'
        self._engine = create_engine(
            self._db_url,
            connect_args={'check_same_thread': False},
        )

    def create_tables(self):
        from src.infrastructure.sqlite.models.user import User  # noqa: F401
        from src.infrastructure.sqlite.models.category import (  # noqa: F401
            Category,
        )
        from src.infrastructure.sqlite.models.location import (  # noqa: F401
            Location,
        )
        from src.infrastructure.sqlite.models.post import Post  # noqa: F401
        from src.infrastructure.sqlite.models.comment import (  # noqa: F401
            Comment,
        )

        Base.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


database = Database()
Base = declarative_base()
