from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        db_path = base_dir / 'db.sqlite3'
        self._db_url = f'sqlite:///{db_path}'
        self._engine = create_engine(
            self._db_url,
            connect_args={'check_same_thread': False},
        )

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
