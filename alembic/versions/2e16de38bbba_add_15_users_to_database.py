"""add 15 users to database

Revision ID: 2e16de38bbba
Revises: 6db7cf1de472
Create Date: 2026-03-26 19:46:28.063898

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
import bcrypt


# revision identifiers, used by Alembic.
revision: str = '2e16de38bbba'
down_revision: Union[str, Sequence[str], None] = '6db7cf1de472'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def hash_password(password: str) -> str:
    """Хеширование пароля."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def upgrade() -> None:
    """Добавить 15 пользователей в базу данных."""
    # Получаем соединение с БД
    conn = op.get_bind()
    
    # Данные пользователей
    users_data = [
        {'username': 'admin', 'email': 'admin@example.com', 'first_name': 'Админ', 'last_name': 'Админов', 'password': 'admin123'},
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'password': 'password123'},
        {'username': 'alex_dev', 'email': 'alex@example.com', 'first_name': 'Александр', 'last_name': 'Разработчиков', 'password': 'password123'},
        {'username': 'maria_writer', 'email': 'maria@example.com', 'first_name': 'Мария', 'last_name': 'Писательская', 'password': 'password123'},
        {'username': 'dmitry_photo', 'email': 'dmitry@example.com', 'first_name': 'Дмитрий', 'last_name': 'Фотографов', 'password': 'password123'},
        {'username': 'elena_travel', 'email': 'elena@example.com', 'first_name': 'Елена', 'last_name': 'Путешественница', 'password': 'password123'},
        {'username': 'maxim_sport', 'email': 'maxim@example.com', 'first_name': 'Максим', 'last_name': 'Спортивный', 'password': 'password123'},
        {'username': 'olga_cook', 'email': 'olga@example.com', 'first_name': 'Ольга', 'last_name': 'Кулинарная', 'password': 'password123'},
        {'username': 'sergey_tech', 'email': 'sergey@example.com', 'first_name': 'Сергей', 'last_name': 'Технический', 'password': 'password123'},
        {'username': 'anna_art', 'email': 'anna@example.com', 'first_name': 'Анна', 'last_name': 'Художественная', 'password': 'password123'},
        {'username': 'ivan_music', 'email': 'ivan@example.com', 'first_name': 'Иван', 'last_name': 'Музыкальный', 'password': 'password123'},
        {'username': 'natasha_design', 'email': 'natasha@example.com', 'first_name': 'Наталья', 'last_name': 'Дизайнерская', 'password': 'password123'},
        {'username': 'artem_code', 'email': 'artem@example.com', 'first_name': 'Артём', 'last_name': 'Программистов', 'password': 'password123'},
        {'username': 'kristina_blog', 'email': 'kristina@example.com', 'first_name': 'Кристина', 'last_name': 'Блогерская', 'password': 'password123'},
    ]
    
    # Вставка пользователей
    for user in users_data:
        conn.execute(
            sa.text("""
                INSERT INTO auth_user (
                    password, last_login, is_superuser, username, 
                    first_name, last_name, email, is_staff, is_active, 
                    date_joined
                ) VALUES (
                    :password, NULL, 0, :username,
                    :first_name, :last_name, :email, 0, 1,
                    :date_joined
                )
            """),
            {
                'password': hash_password(user['password']),
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'date_joined': datetime.now().isoformat(),
            }
        )
    
    conn.commit()


def downgrade() -> None:
    """Удалить добавленных пользователей."""
    conn = op.get_bind()
    
    usernames = [
        'admin', 'john_doe', 'jane_smith', 'alex_dev', 'maria_writer',
        'dmitry_photo', 'elena_travel', 'maxim_sport', 'olga_cook',
        'sergey_tech', 'anna_art', 'ivan_music', 'natasha_design',
        'artem_code', 'kristina_blog',
    ]
    
    # Удаление пользователей по username
    conn.execute(
        sa.text("DELETE FROM auth_user WHERE username IN :usernames"),
        {'usernames': tuple(usernames)}
    )
    
    conn.commit()
