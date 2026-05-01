from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class Database:
    def __init__(self):
        self._db_url = settings.DATABASE_URL
        logger.info(f"Подключение к базе данных: {self._db_url}")
        self._engine = create_engine(
            self._db_url,
            connect_args={'check_same_thread': False} if 'sqlite' in self._db_url else {},
        )

    @contextmanager
    def session(self):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        try:
            logger.debug("Открыта сессия БД")
            yield session
            session.commit()
            logger.debug("Сессия БД закоммичена")
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка в сессии БД: {e}")
            raise
        finally:
            session.close()
            logger.debug("Сессия БД закрыта")


database = Database()
