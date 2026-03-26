"""add initial data

Revision ID: 57e2e0cab439
Revises: 6db7cf1de472
Create Date: 2026-03-26 23:01:48.813271

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
import bcrypt


# revision identifiers, used by Alembic.
revision: str = '57e2e0cab439'
down_revision: Union[str, Sequence[str], None] = '6db7cf1de472'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def upgrade() -> None:
    conn = op.get_bind()
    now = datetime.now().isoformat()
    
    # Users (15)
    users_data = [
        ('admin', 'admin@example.com', 'Админ', 'Админов', 'admin123'),
        ('john_doe', 'john@example.com', 'John', 'Doe', 'password123'),
        ('jane_smith', 'jane@example.com', 'Jane', 'Smith', 'password123'),
        ('alex_dev', 'alex@example.com', 'Александр', 'Разработчиков', 'password123'),
        ('maria_writer', 'maria@example.com', 'Мария', 'Писательская', 'password123'),
        ('dmitry_photo', 'dmitry@example.com', 'Дмитрий', 'Фотографов', 'password123'),
        ('elena_travel', 'elena@example.com', 'Елена', 'Путешественница', 'password123'),
        ('maxim_sport', 'maxim@example.com', 'Максим', 'Спортивный', 'password123'),
        ('olga_cook', 'olga@example.com', 'Ольга', 'Кулинарная', 'password123'),
        ('sergey_tech', 'sergey@example.com', 'Сергей', 'Технический', 'password123'),
        ('anna_art', 'anna@example.com', 'Анна', 'Художественная', 'password123'),
        ('ivan_music', 'ivan@example.com', 'Иван', 'Музыкальный', 'password123'),
        ('natasha_design', 'natasha@example.com', 'Наталья', 'Дизайнерская', 'password123'),
        ('artem_code', 'artem@example.com', 'Артём', 'Программистов', 'password123'),
        ('kristina_blog', 'kristina@example.com', 'Кристина', 'Блогерская', 'password123'),
    ]
    
    user_ids = []
    for username, email, first_name, last_name, password in users_data:
        conn.execute(
            sa.text("""
                INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
                VALUES (:password, NULL, 0, :username, :first_name, :last_name, :email, 0, 1, :date_joined)
            """),
            {'password': hash_password(password), 'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'date_joined': now}
        )
        user_ids.append(conn.execute(sa.text("SELECT last_insert_rowid()")).scalar())
    
    # Categories (4)
    categories_data = [
        ('Технологии', 'tech', 'Всё о технологиях, программировании и инновациях'),
        ('Путешествия', 'travel', 'Рассказы о путешествиях по всему миру'),
        ('Кулинария', 'cooking', 'Рецепты и кулинарные эксперименты'),
        ('Спорт', 'sport', 'Спортивные новости и достижения'),
    ]
    
    category_ids = []
    for title, slug, description in categories_data:
        conn.execute(
            sa.text("INSERT INTO blog_category (created_at, is_published, title, description, slug) VALUES (:created_at, 1, :title, :description, :slug)"),
            {'created_at': now, 'title': title, 'description': description, 'slug': slug}
        )
        category_ids.append(conn.execute(sa.text("SELECT last_insert_rowid()")).scalar())
    
    # Locations (5)
    locations_data = ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург']
    
    location_ids = []
    for name in locations_data:
        conn.execute(
            sa.text("INSERT INTO blog_location (created_at, is_published, name) VALUES (:created_at, 1, :name)"),
            {'created_at': now, 'name': name}
        )
        location_ids.append(conn.execute(sa.text("SELECT last_insert_rowid()")).scalar())
    
    # Posts (10)
    posts_data = [
        ('Как я провёл лето', 'Это был незабываемый опыт!', 1, 1, 1),
        ('Мои впечатления о конференции', 'Хочу поделиться своими мыслями.', 2, 2, 1),
        ('Топ-10 мест для посещения', 'Долго готовился к этому.', 3, 3, 2),
        ('Рецепт идеальной пиццы', 'В этой статье я собрал все наблюдения.', 4, 4, 3),
        ('Почему стоит изучать Python', 'Если вы задумывались — читайте!', 5, 1, 1),
        ('Путешествие на Байкал', 'Никогда не думал что так интересно.', 6, 2, 2),
        ('Обзор нового смартфона', 'Делюсь опытом.', 7, 3, 1),
        ('Мой первый марафон', 'Это изменило моё представление.', 8, 4, 4),
        ('Секреты успешного стартапа', 'Рекомендую попробовать!', 9, 1, 1),
        ('Зимние каникулы в горах', 'История о том, как идея изменила всё.', 10, 2, 2),
    ]
    
    post_ids = []
    for title, text, author_idx, location_idx, category_idx in posts_data:
        pub_date = (datetime.now()).isoformat()
        conn.execute(
            sa.text("""
                INSERT INTO blog_post (created_at, is_published, title, text, pub_date, author_id, location_id, category_id, image)
                VALUES (:created_at, 1, :title, :text, :pub_date, :author_id, :location_id, :category_id, '')
            """),
            {'created_at': now, 'title': title, 'text': text, 'pub_date': pub_date, 'author_id': user_ids[author_idx-1], 'location_id': location_ids[location_idx-1], 'category_id': category_ids[category_idx-1]}
        )
        post_ids.append(conn.execute(sa.text("SELECT last_insert_rowid()")).scalar())
    
    # Comments (15)
    comments_data = [
        ('Отличная статья!', 1, 2), ('Очень полезно.', 1, 3), ('Можно подробнее?', 2, 4),
        ('Согласен на 100%!', 2, 5), ('Интересный подход.', 3, 6), ('Жду продолжения!', 3, 7),
        ('Есть замечания.', 4, 8), ('Лучшее что читал!', 4, 9), ('Спасибо за труды!', 5, 10),
        ('Буду рекомендовать.', 5, 1), ('Класс!', 6, 2), ('Спасибо за рецепт!', 7, 3),
        ('Отличный обзор.', 8, 4), ('Вдохновляет!', 9, 5), ('Полезно для начинающих.', 10, 6),
    ]
    
    for text, post_idx, author_idx in comments_data:
        conn.execute(
            sa.text("INSERT INTO blog_comment (created_at, is_published, post_id, text, author_id) VALUES (:created_at, 1, :post_id, :text, :author_id)"),
            {'created_at': now, 'post_id': post_ids[post_idx-1], 'text': text, 'author_id': user_ids[author_idx-1]}
        )
    
    conn.commit()


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM blog_comment"))
    conn.execute(sa.text("DELETE FROM blog_post"))
    conn.execute(sa.text("DELETE FROM blog_location"))
    conn.execute(sa.text("DELETE FROM blog_category"))
    conn.execute(sa.text("DELETE FROM auth_user"))
    conn.commit()
