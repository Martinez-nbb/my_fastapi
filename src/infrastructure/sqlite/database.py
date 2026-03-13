from contextlib import contextmanager
from pathlib import Path

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        # Путь к базе данных Django
        # Для использования Django БД раскомментируйте строку ниже и укажите правильный путь
        # base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        # db_path = base_dir / 'django_sprint4' / 'db.sqlite3'

        # Временная БД для тестирования - в корне проекта my_fastapi
        base_dir = Path(__file__).resolve().parent.parent.parent.parent  # my_fastapi/
        db_path = base_dir / 'db.sqlite3'
        
        # Используем абсолютный путь для SQLite
        self._db_url = f'sqlite:///{db_path.absolute()}'
        self._engine = create_engine(self._db_url, echo=False)

    def create_tables(self):
        # Импортируем Base и модели для регистрации в metadata
        from src.infrastructure.sqlite.metadata import Base
        from src.infrastructure.sqlite.models import User, Category, Location, Post, Comment

        Base.metadata.create_all(bind=self._engine)
        
        # Явно делаем commit для SQLite
        with self._engine.connect() as conn:
            conn.commit()

    @contextmanager
    def session(self):
        connection = self._engine.connect()

        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
            connection.close()
        except Exception:
            session.rollback()
            raise


database = Database()
