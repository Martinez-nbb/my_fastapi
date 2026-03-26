"""populate all tables with initial data

Revision ID: 4d1d35529cb4
Revises: 6db7cf1de472
Create Date: 2026-03-26 20:00:00.000000

"""
from typing import Sequence, Union
from datetime import datetime, timedelta

from alembic import op
import sqlalchemy as sa
import bcrypt


# revision identifiers, used by Alembic.
revision: str = '4d1d35529cb4'
down_revision: Union[str, Sequence[str], None] = '6db7cf1de472'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def hash_password(password: str) -> str:
    """Хеширование пароля."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def upgrade() -> None:
    """Наполнить все таблицы начальными данными."""
    conn = op.get_bind()
    now = datetime.now().isoformat()
    
    # ==================== USERS (15 пользователей) ====================
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
    
    user_ids = []
    for user in users_data:
        result = conn.execute(
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
                'date_joined': now,
            }
        )
        # Получаем ID последнего вставленного пользователя
        user_id = conn.execute(sa.text("SELECT last_insert_rowid()")).scalar()
        user_ids.append(user_id)
    
    # ==================== CATEGORIES (4 категории) ====================
    categories_data = [
        ('Технологии', 'tech', 'Всё о технологиях, программировании и инновациях'),
        ('Путешествия', 'travel', 'Рассказы о путешествиях по всему миру'),
        ('Кулинария', 'cooking', 'Рецепты и кулинарные эксперименты'),
        ('Спорт', 'sport', 'Спортивные новости и достижения'),
    ]
    
    category_ids = []
    for title, slug, description in categories_data:
        conn.execute(
            sa.text("""
                INSERT INTO blog_category (created_at, is_published, title, description, slug)
                VALUES (:created_at, 1, :title, :description, :slug)
            """),
            {
                'created_at': now,
                'title': title,
                'description': description,
                'slug': slug,
            }
        )
        cat_id = conn.execute(sa.text("SELECT last_insert_rowid()")).scalar()
        category_ids.append(cat_id)
    
    # ==================== LOCATIONS (5 местоположений) ====================
    locations_data = [
        'Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург',
    ]
    
    location_ids = []
    for name in locations_data:
        conn.execute(
            sa.text("""
                INSERT INTO blog_location (created_at, is_published, name)
                VALUES (:created_at, 1, :name)
            """),
            {'created_at': now, 'name': name}
        )
        loc_id = conn.execute(sa.text("SELECT last_insert_rowid()")).scalar()
        location_ids.append(loc_id)
    
    # ==================== POSTS (10 публикаций) ====================
    posts_data = [
        ('Как я провёл лето', 'Это был незабываемый опыт! Много новых впечатлений и встреч.', 1, 1, 1),
        ('Мои впечатления о конференции', 'Хочу поделиться своими мыслями об этом замечательном событии.', 2, 2, 1),
        ('Топ-10 мест для посещения', 'Долго готовился к этому и наконец могу рассказать.', 3, 3, 2),
        ('Рецепт идеальной пиццы', 'В этой статье я собрал все свои наблюдения и выводы.', 4, 4, 3),
        ('Почему стоит изучать Python', 'Если вы когда-нибудь задумывались об этом — читайте дальше!', 5, 1, 1),
        ('Путешествие на Байкал', 'Никогда не думал, что это окажется так интересно.', 6, 2, 2),
        ('Обзор нового смартфона', 'Делюсь своим опытом и надеюсь, что кому-то пригодится.', 7, 3, 1),
        ('Мой первый марафон', 'Это изменило моё представление о многих вещах.', 8, 4, 4),
        ('Секреты успешного стартапа', 'Рекомендую попробовать каждому, не пожалеете!', 9, 1, 1),
        ('Зимние каникулы в горах', 'История о том, как одна идея изменила всё.', 10, 2, 2),
    ]
    
    post_ids = []
    for title, text, author_idx, location_idx, category_idx in posts_data:
        pub_date = (datetime.now() - timedelta(days=author_idx * 10)).isoformat()
        conn.execute(
            sa.text("""
                INSERT INTO blog_post (
                    created_at, is_published, title, text, pub_date,
                    author_id, location_id, category_id, image
                ) VALUES (
                    :created_at, 1, :title, :text, :pub_date,
                    :author_id, :location_id, :category_id, ''
                )
            """),
            {
                'created_at': now,
                'title': title,
                'text': text,
                'pub_date': pub_date,
                'author_id': user_ids[author_idx - 1],
                'location_id': location_ids[location_idx - 1],
                'category_id': category_ids[category_idx - 1],
            }
        )
        post_id = conn.execute(sa.text("SELECT last_insert_rowid()")).scalar()
        post_ids.append(post_id)
    
    # ==================== COMMENTS (15 комментариев) ====================
    comments_data = [
        ('Отличная статья, спасибо!', 1, 2),
        ('Очень полезно, взял на заметку.', 1, 3),
        ('А можно подробнее об этом моменте?', 2, 4),
        ('Согласен с автором на 100%!', 2, 5),
        ('Интересный подход, надо попробовать.', 3, 6),
        ('Жду продолжения темы!', 3, 7),
        ('Есть небольшие замечания, но в целом хорошо.', 4, 8),
        ('Лучшее, что читал по этой теме!', 4, 9),
        ('Спасибо за труды!', 5, 10),
        ('Буду рекомендовать друзьям.', 5, 1),
        ('Класс! Обязательно попробую.', 6, 2),
        ('Спасибо за рецепт!', 7, 3),
        ('Отличный обзор, помогло с выбором.', 8, 4),
        ('Вдохновляет!', 9, 5),
        ('Полезно для начинающих.', 10, 6),
    ]
    
    for text, post_idx, author_idx in comments_data:
        conn.execute(
            sa.text("""
                INSERT INTO blog_comment (
                    created_at, is_published, post_id, text, author_id
                ) VALUES (
                    :created_at, 1, :post_id, :text, :author_id
                )
            """),
            {
                'created_at': now,
                'post_id': post_ids[post_idx - 1],
                'text': text,
                'author_id': user_ids[author_idx - 1],
            }
        )
    
    conn.commit()
    
    # Вывод статистики
    print("=" * 50)
    print("БД успешно заполнена!")
    print("=" * 50)
    print(f"  Пользователей: {len(user_ids)}")
    print(f"  Категорий: {len(category_ids)}")
    print(f"  Местоположений: {len(location_ids)}")
    print(f"  Постов: {len(post_ids)}")
    print(f"  Комментариев: {len(comments_data)}")


def downgrade() -> None:
    """Очистить все таблицы от данных."""
    conn = op.get_bind()
    
    # Удаляем данные в порядке, обратном зависимостям
    conn.execute(sa.text("DELETE FROM blog_comment"))
    conn.execute(sa.text("DELETE FROM blog_post"))
    conn.execute(sa.text("DELETE FROM blog_location"))
    conn.execute(sa.text("DELETE FROM blog_category"))
    conn.execute(sa.text("DELETE FROM auth_user"))
    
    conn.commit()
