"""add seed data

Revision ID: 4caf9896c3cc
Revises: d95a43aeae2a
Create Date: 2026-05-23 09:09:11.375033

"""
from datetime import datetime, timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4caf9896c3cc'
down_revision: Union[str, Sequence[str], None] = 'd95a43aeae2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _schema(table: str) -> str:
    return f'application.{table}'


def upgrade() -> None:
    now = datetime.now()
    bind = op.get_bind()

    # --- users ---
    users_data = [
        ('admin', '$2b$12$K0WuBOGoWcdkXsCPSc6pj.D3etXVcLjIywaeXRdrAt7ScZKYbmd.i',
         'admin@example.com', 'Admin', 'User', True, True, True),
        ('john_doe', '$2b$12$dtj2WrhCakbcFCCVwzT9Z.vcMAuntI56BIuomnRzWZc6lZ394zK5O',
         'john@example.com', 'John', 'Doe', False, False, True),
        ('jane_smith', '$2b$12$aeexWOcYl9YJuGj6W7C8Aum1jLflVoJxGEyyB45i2zA2x0uNjrff2',
         'jane@example.com', 'Jane', 'Smith', False, True, True),
        ('bob_wilson', '$2b$12$SB1Uq75aTDBZEm9Zcejd3.Na3hDKQSSv/P1631swDmW6T9dY0D9h6',
         'bob@example.com', 'Bob', 'Wilson', False, False, True),
        ('alice_green', '$2b$12$fZBwTbyJIoY37R38Zq9CRuq4AGWxndtO6jJl40PWaBLtrqvJkSbQ6',
         'alice@example.com', 'Alice', 'Green', False, False, False),
    ]
    for username, password, email, first_name, last_name, is_superuser, is_staff, is_active in users_data:
        exists = bind.execute(
            sa.text(f"SELECT 1 FROM {_schema('auth_user')} WHERE username = :username"),
            {'username': username}
        ).scalar()
        if not exists:
            bind.execute(
                sa.text(f"""
                    INSERT INTO {_schema('auth_user')}
                        (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
                    VALUES (:password, NULL, :is_superuser, :username, :first_name, :last_name, :email, :is_staff, :is_active, :date_joined)
                """),
                {
                    'password': password,
                    'is_superuser': is_superuser,
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_staff': is_staff,
                    'is_active': is_active,
                    'date_joined': now,
                }
            )

    # --- categories ---
    categories_data = [
        ('Technology', 'technology', 'News and articles about technology, gadgets, and software', True),
        ('Travel', 'travel', 'Travel guides, tips, and stories from around the world', True),
        ('Food & Cooking', 'food', 'Recipes, cooking tips, and food culture', True),
        ('Science', 'science', 'Scientific discoveries, research, and education', True),
        ('Sports', 'sports', 'Sports news, analysis, and commentary', False),
    ]
    for title, slug, description, is_published in categories_data:
        exists = bind.execute(
            sa.text(f"SELECT 1 FROM {_schema('blog_category')} WHERE slug = :slug"),
            {'slug': slug}
        ).scalar()
        if not exists:
            bind.execute(
                sa.text(f"""
                    INSERT INTO {_schema('blog_category')} (created_at, is_published, title, description, slug)
                    VALUES (:created_at, :is_published, :title, :description, :slug)
                """),
                {
                    'created_at': now,
                    'is_published': is_published,
                    'title': title,
                    'description': description,
                    'slug': slug,
                }
            )

    # --- locations ---
    locations_data = [
        ('Moscow', True),
        ('Saint Petersburg', True),
        ('London', True),
        ('Tokyo', True),
        ('New York', True),
        ('Paris', True),
        ('Berlin', False),
    ]
    for name, is_published in locations_data:
        exists = bind.execute(
            sa.text(f"SELECT 1 FROM {_schema('blog_location')} WHERE name = :name"),
            {'name': name}
        ).scalar()
        if not exists:
            bind.execute(
                sa.text(f"""
                    INSERT INTO {_schema('blog_location')} (created_at, is_published, name)
                    VALUES (:created_at, :is_published, :name)
                """),
                {
                    'created_at': now,
                    'is_published': is_published,
                    'name': name,
                }
            )

    # --- resolve FK refs ---
    def get_id(table: str, field: str, value: str) -> int | None:
        return bind.execute(
            sa.text(f"SELECT id FROM {_schema(table)} WHERE {field} = :value"),
            {'value': value}
        ).scalar()

    admin_id = get_id('auth_user', 'username', 'admin')
    john_id = get_id('auth_user', 'username', 'john_doe')
    jane_id = get_id('auth_user', 'username', 'jane_smith')
    bob_id = get_id('auth_user', 'username', 'bob_wilson')

    tech_id = get_id('blog_category', 'slug', 'technology')
    travel_id = get_id('blog_category', 'slug', 'travel')
    food_id = get_id('blog_category', 'slug', 'food')
    science_id = get_id('blog_category', 'slug', 'science')
    sports_id = get_id('blog_category', 'slug', 'sports')

    moscow_id = get_id('blog_location', 'name', 'Moscow')
    spb_id = get_id('blog_location', 'name', 'Saint Petersburg')
    tokyo_id = get_id('blog_location', 'name', 'Tokyo')
    paris_id = get_id('blog_location', 'name', 'Paris')
    london_id = get_id('blog_location', 'name', 'London')
    nyc_id = get_id('blog_location', 'name', 'New York')
    berlin_id = get_id('blog_location', 'name', 'Berlin')

    # --- posts ---
    posts_data = [
        ('Getting Started with Python FastAPI',
         'FastAPI is a modern web framework for building APIs with Python.',
         now - timedelta(days=30), admin_id, tech_id, moscow_id, True),
        ('Exploring the Streets of Tokyo',
         'Tokyo is a city that never sleeps.',
         now - timedelta(days=25), john_id, travel_id, tokyo_id, True),
        ('Best Pasta Recipes for Beginners',
         'Making pasta from scratch is easier than you think.',
         now - timedelta(days=20), jane_id, food_id, paris_id, True),
        ('Quantum Computing Explained',
         'Quantum computing represents a paradigm shift.',
         now - timedelta(days=15), admin_id, science_id, None, True),
        ('A Weekend in Paris',
         'Paris is always a good idea.',
         now - timedelta(days=10), john_id, travel_id, paris_id, True),
        ('Introduction to Machine Learning',
         'Machine learning is transforming industries.',
         now - timedelta(days=5), jane_id, tech_id, spb_id, False),
        ('The Art of Sourdough Bread',
         'Sourdough bread has a rich history.',
         now - timedelta(days=2), bob_id, food_id, None, True),
    ]

    post_ids = []
    for title, text, pub_date, author_id, category_id, location_id, is_published in posts_data:
        exists = bind.execute(
            sa.text(f"SELECT 1 FROM {_schema('blog_post')} WHERE title = :title"),
            {'title': title}
        ).scalar()
        if not exists:
            result = bind.execute(
                sa.text(f"""
                    INSERT INTO {_schema('blog_post')} (created_at, is_published, title, text, pub_date, author_id, location_id, category_id)
                    VALUES (:created_at, :is_published, :title, :text, :pub_date, :author_id, :location_id, :category_id)
                    RETURNING id
                """),
                {
                    'created_at': now,
                    'is_published': is_published,
                    'title': title,
                    'text': text,
                    'pub_date': pub_date,
                    'author_id': author_id,
                    'location_id': location_id,
                    'category_id': category_id,
                }
            )
            post_ids.append(result.scalar())
        else:
            pid = bind.execute(
                sa.text(f"SELECT id FROM {_schema('blog_post')} WHERE title = :title"),
                {'title': title}
            ).scalar()
            post_ids.append(pid)

    # --- comments ---
    comments_texts = [
        ('Great article! Very helpful for beginners.', 0),
        ('I have been using FastAPI for a while and it is amazing.', 0),
        ('Tokyo is my favorite city! Thanks for the tips.', 1),
        ('I am planning a trip to Japan next year. Saving this!', 1),
        ('These recipes look delicious. Trying the carbonara tonight!', 2),
        ('Can you recommend a good pasta machine?', 2),
        ('Quantum computing is fascinating. Great explanation!', 3),
        ('Paris in spring is magical. Great itinerary!', 4),
        ('I would add Montmartre to the list as well.', 4),
        ('Sourdough is my new obsession. Thanks for the guide!', 6),
    ]
    user_ids_for_comments = [admin_id, john_id, jane_id, bob_id, admin_id, john_id, jane_id, bob_id, admin_id, john_id]

    for (text, post_idx), author_id in zip(comments_texts, user_ids_for_comments):
        post_id = post_ids[post_idx]
        exists = bind.execute(
            sa.text(f"SELECT 1 FROM {_schema('blog_comment')} WHERE text = :text AND post_id = :post_id"),
            {'text': text, 'post_id': post_id}
        ).scalar()
        if not exists:
            bind.execute(
                sa.text(f"""
                    INSERT INTO {_schema('blog_comment')} (created_at, is_published, post_id, text, author_id)
                    VALUES (:created_at, :is_published, :post_id, :text, :author_id)
                """),
                {
                    'created_at': now,
                    'is_published': True,
                    'post_id': post_id,
                    'text': text,
                    'author_id': author_id,
                }
            )


def downgrade() -> None:
    bind = op.get_bind()

    usernames = ['admin', 'john_doe', 'jane_smith', 'bob_wilson', 'alice_green']
    for username in usernames:
        bind.execute(
            sa.text(f"DELETE FROM {_schema('blog_comment')} "
                    f"WHERE author_id = (SELECT id FROM {_schema('auth_user')} WHERE username = :username)"),
            {'username': username}
        )
        bind.execute(
            sa.text(f"DELETE FROM {_schema('blog_post')} "
                    f"WHERE author_id = (SELECT id FROM {_schema('auth_user')} WHERE username = :username)"),
            {'username': username}
        )

    slugs = ['technology', 'travel', 'food', 'science', 'sports']
    for slug in slugs:
        bind.execute(
            sa.text(f"DELETE FROM {_schema('blog_category')} WHERE slug = :slug"),
            {'slug': slug}
        )

    names = ['Moscow', 'Saint Petersburg', 'London', 'Tokyo', 'New York', 'Paris', 'Berlin']
    for name in names:
        bind.execute(
            sa.text(f"DELETE FROM {_schema('blog_location')} WHERE name = :name"),
            {'name': name}
        )

    for username in usernames:
        bind.execute(
            sa.text(f"DELETE FROM {_schema('auth_user')} WHERE username = :username"),
            {'username': username}
        )
