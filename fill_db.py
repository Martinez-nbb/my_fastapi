import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

import bcrypt

sys.path.insert(0, str(Path(__file__).parent))

from src.infrastructure.sqlite.database import database  # noqa: E402
from src.infrastructure.sqlite.models.user import User  # noqa: E402
from src.infrastructure.sqlite.models.category import Category  # noqa: E402
from src.infrastructure.sqlite.models.location import Location  # noqa: E402
from src.infrastructure.sqlite.models.post import Post  # noqa: E402
from src.infrastructure.sqlite.models.comment import Comment  # noqa: E402


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def clear_db():
    with database.session() as session:
        session.query(Comment).delete()
        session.query(Post).delete()
        session.query(Location).delete()
        session.query(Category).delete()
        session.query(User).delete()
        session.commit()
    print("БД очищена")


def create_users(count: int = 10) -> list[int]:
    first_names = [
        'Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей',
        'Алексей', 'Артём', 'Илья', 'Кирилл', 'Михаил',
        'Елена', 'Ольга', 'Анна', 'Мария', 'Екатерина',
        'Наталья', 'Ирина', 'Кристина', 'Юлия', 'Анастасия'
    ]
    last_names = [
        'Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев',
        'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Фёдоров',
        'Морозов', 'Волков', 'Алексеев', 'Лебедев', 'Семёнов'
    ]
    usernames = set()

    user_ids = []
    with database.session() as session:
        for i in range(count):
            while True:
                username = f"user{random.randint(1, 999)}"
                if username not in usernames:
                    usernames.add(username)
                    break

            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            user = User(
                username=username,
                email=f"{username}@example.com",
                password=hash_password("password123"),
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            session.add(user)
            session.flush()
            user_ids.append(user.id)

        session.commit()

    print(f"Создано пользователей: {len(user_ids)}")
    return user_ids


def create_categories(count: int = 4) -> list[int]:
    categories_data = [
        ('Технологии', 'tech',
         'Всё о технологиях, программировании и инновациях'),
        ('Путешествия', 'travel',
         'Рассказы о путешествиях по всему миру'),
        ('Кулинария', 'cooking',
         'Рецепты и кулинарные эксперименты'),
        ('Спорт', 'sport', 'Спортивные новости и достижения'),
    ]

    category_ids = []
    with database.session() as session:
        for i in range(count):
            title, slug, description = categories_data[
                i % len(categories_data)]
            category = Category(
                title=title,
                slug=f"{slug}-{i}" if i >= len(categories_data) else slug,
                description=description,
                is_published=True,
                created_at=datetime.now(),
            )
            session.add(category)
            session.flush()
            category_ids.append(category.id)

        session.commit()

    print(f"Создано категорий: {len(category_ids)}")
    return category_ids


def create_locations(count: int = 5) -> list[int]:
    locations_data = [
        'Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск',
        'Екатеринбург', 'Владивосток', 'Сочи', 'Калининград'
    ]

    location_ids = []
    with database.session() as session:
        for i in range(count):
            name = locations_data[i % len(locations_data)]
            location = Location(
                name=f"{name} {i+1}" if i >= len(locations_data) else name,
                is_published=True,
                created_at=datetime.now(),
            )
            session.add(location)
            session.flush()
            location_ids.append(location.id)

        session.commit()

    print(f"Создано местоположений: {len(location_ids)}")
    return location_ids


def create_posts(user_ids: list[int], category_ids: list[int],
                 location_ids: list[int], count: int = 13) -> list[int]:
    titles = [
        'Как я провёл лето', 'Мои впечатления о конференции',
        'Топ-10 мест для посещения', 'Рецепт идеальной пиццы',
        'Почему стоит изучать Python', 'Путешествие на Байкал',
        'Обзор нового смартфона', 'Мой первый марафон',
        'Секреты успешного стартапа', 'Зимние каникулы в горах',
        'Как научиться программировать', 'Лучшие книги 2025 года',
        'Фотопрогулка по городу', 'Велопутешествие по Европе',
        'Мастер-класс по фотографии',
    ]

    texts = [
        'Это был незабываемый опыт! Много новых впечатлений и встреч.',
        'Хочу поделиться своими мыслями об этом замечательном событии.',
        'Долго готовился к этому и наконец могу рассказать.',
        'В этой статье я собрал все свои наблюдения и выводы.',
        'Если вы когда-нибудь задумывались об этом — читайте дальше!',
        'Никогда не думал, что это окажется так интересно.',
        'Делюсь своим опытом и надеюсь, что кому-то пригодится.',
        'Это изменило моё представление о многих вещах.',
        'Рекомендую попробовать каждому, не пожалеете!',
        'История о том, как одна идея изменила всё.',
        'Подробный разбор с примерами и скриншотами.',
        'Мои личные наблюдения и выводы после месяца экспериментов.',
        'Небольшой гайд для начинающих с полезными советами.',
    ]

    posts_ids = []
    with database.session() as session:
        for i in range(count):
            post = Post(
                title=random.choice(titles),
                text=random.choice(texts),
                pub_date=datetime.now() - timedelta(
                    days=random.randint(0, 365)),
                author_id=random.choice(user_ids),
                location_id=random.choice(location_ids)
                if random.random() > 0.3 else None,
                category_id=random.choice(category_ids)
                if random.random() > 0.2 else None,
                is_published=random.random() > 0.1,
                created_at=datetime.now(),
            )
            session.add(post)
            session.flush()
            posts_ids.append(post.id)

        session.commit()

    print(f"Создано постов: {len(posts_ids)}")
    return posts_ids


def create_comments(user_ids: list[int], post_ids: list[int],
                    count: int = 8):
    comment_texts = [
        'Отличная статья, спасибо!',
        'Очень полезно, взял на заметку.',
        'А можно подробнее об этом моменте?',
        'Согласен с автором на 100%!',
        'Интересный подход, надо попробовать.',
        'Жду продолжения темы!',
        'Есть небольшие замечания, но в целом хорошо.',
        'Лучшее, что читал по этой теме!',
        'Спасибо за труды!',
        'Буду рекомендовать друзьям.',
    ]

    comments = []
    with database.session() as session:
        for i in range(count):
            comment = Comment(
                text=random.choice(comment_texts),
                post_id=random.choice(post_ids),
                author_id=random.choice(user_ids),
                is_published=True,
                created_at=datetime.now(),
            )
            session.add(comment)
            comments.append(comment)

        session.commit()

    print(f"Создано комментариев: {len(comments)}")


def main():
    print("=" * 50)
    print("Заполнение БД случайными данными")
    print("=" * 50)

    clear_db()

    user_ids = create_users(10)
    category_ids = create_categories(4)
    location_ids = create_locations(5)
    post_ids = create_posts(
        user_ids, category_ids, location_ids, 13)
    create_comments(user_ids, post_ids, 8)

    print("=" * 50)
    print("БД успешно заполнена!")
    print("=" * 50)

    with database.session() as session:
        print("\nСтатистика:")
        print(f"  Пользователей: {session.query(User).count()}")
        print(f"  Категорий: {session.query(Category).count()}")
        print(
            f"  Местоположений: {session.query(Location).count()}")
        print(f"  Постов: {session.query(Post).count()}")
        print(f"  Комментариев: {session.query(Comment).count()}")


if __name__ == '__main__':
    main()
