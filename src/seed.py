import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from sqlalchemy import delete

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.models.comment_image import CommentImage
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.models.post_image import PostImage
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.resources.auth import get_password_hash
from src.schemas.users import UserCreateSchema
from src.schemas.categories import CategoryCreateSchema
from src.schemas.locations import LocationCreateSchema
from src.schemas.posts import PostCreateSchema, PostImageCreateSchema
from src.schemas.comments import CommentCreateSchema

logger = logging.getLogger(__name__)


async def clear_data():
    async with database.session() as session:
        await session.execute(delete(CommentImage))
        await session.execute(delete(PostImage))
        await session.execute(delete(Comment))
        await session.execute(delete(Post))
        await session.execute(delete(Category))
        await session.execute(delete(Location))
        await session.execute(delete(User))
        logger.info("Existing data cleared")


async def seed_users():
    repo = UserRepository()
    users_data = [
        {
            "username": "admin",
            "password": "admin123",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
        },
        {
            "username": "john_doe",
            "password": "password123",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
        },
        {
            "username": "jane_smith",
            "password": "password123",
            "email": "jane@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "is_superuser": False,
            "is_staff": True,
            "is_active": True,
        },
        {
            "username": "bob_wilson",
            "password": "password123",
            "email": "bob@example.com",
            "first_name": "Bob",
            "last_name": "Wilson",
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
        },
        {
            "username": "alice_green",
            "password": "password123",
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Green",
            "is_superuser": False,
            "is_staff": False,
            "is_active": False,
        },
    ]

    created = []
    for data in users_data:
        password = data.pop("password")
        hashed = get_password_hash(password)
        schema = UserCreateSchema(**data, password=hashed)
        async with database.session() as session:
            try:
                user = await repo.create(session=session, data=schema)
                created.append(user)
                logger.info(f"User created: {user.username} (id={user.id})")
            except Exception as e:
                logger.warning(f"User {data['username']} skipped: {e}")
    return created


async def seed_categories():
    repo = CategoryRepository()
    categories_data = [
        {"title": "Technology", "slug": "technology", "description": "News and articles about technology, gadgets, and software", "is_published": True},
        {"title": "Travel", "slug": "travel", "description": "Travel guides, tips, and stories from around the world", "is_published": True},
        {"title": "Food & Cooking", "slug": "food", "description": "Recipes, cooking tips, and food culture", "is_published": True},
        {"title": "Science", "slug": "science", "description": "Scientific discoveries, research, and education", "is_published": True},
        {"title": "Sports", "slug": "sports", "description": "Sports news, analysis, and commentary", "is_published": False},
    ]

    created = []
    for data in categories_data:
        schema = CategoryCreateSchema(**data)
        async with database.session() as session:
            try:
                category = await repo.create(session=session, data=schema)
                created.append(category)
                logger.info(f"Category created: {category.title} (id={category.id})")
            except Exception as e:
                logger.warning(f"Category {data['title']} skipped: {e}")
    return created


async def seed_locations():
    repo = LocationRepository()
    locations_data = [
        {"name": "Moscow", "is_published": True},
        {"name": "Saint Petersburg", "is_published": True},
        {"name": "London", "is_published": True},
        {"name": "Tokyo", "is_published": True},
        {"name": "New York", "is_published": True},
        {"name": "Paris", "is_published": True},
        {"name": "Berlin", "is_published": False},
    ]

    created = []
    for data in locations_data:
        schema = LocationCreateSchema(**data)
        async with database.session() as session:
            try:
                location = await repo.create(session=session, data=schema)
                created.append(location)
                logger.info(f"Location created: {location.name} (id={location.id})")
            except Exception as e:
                logger.warning(f"Location {data['name']} skipped: {e}")
    return created


async def seed_posts(users, categories, locations):
    repo = PostRepository()

    now = datetime.now()
    posts_data = [
        {
            "title": "Getting Started with Python FastAPI",
            "text": "FastAPI is a modern web framework for building APIs with Python. It is built on top of Starlette and Pydantic, providing automatic OpenAPI documentation, validation, and async support. In this post, we will explore how to set up a FastAPI project and create your first endpoint.",
            "pub_date": now - timedelta(days=30),
            "author_id": users[0].id,
            "category_id": categories[0].id,
            "location_id": locations[0].id,
            "is_published": True,
        },
        {
            "title": "Exploring the Streets of Tokyo",
            "text": "Tokyo is a city that never sleeps. From the neon-lit streets of Shibuya to the serene gardens of Meiji Shrine, there is always something new to discover. The public transport system is incredibly efficient, making it easy to explore different neighborhoods.",
            "pub_date": now - timedelta(days=25),
            "author_id": users[1].id,
            "category_id": categories[1].id,
            "location_id": locations[3].id,
            "is_published": True,
        },
        {
            "title": "Best Pasta Recipes for Beginners",
            "text": "Making pasta from scratch is easier than you think. With just a few ingredients – flour, eggs, and salt – you can create delicious homemade pasta. Here are some simple recipes to get you started on your culinary journey.",
            "pub_date": now - timedelta(days=20),
            "author_id": users[2].id,
            "category_id": categories[2].id,
            "location_id": locations[5].id,
            "is_published": True,
        },
        {
            "title": "Quantum Computing Explained",
            "text": "Quantum computing represents a paradigm shift in how we process information. Unlike classical bits, qubits can exist in multiple states simultaneously, enabling computations that would take classical computers millions of years to complete.",
            "pub_date": now - timedelta(days=15),
            "author_id": users[0].id,
            "category_id": categories[3].id,
            "location_id": None,
            "is_published": True,
        },
        {
            "title": "A Weekend in Paris",
            "text": "Paris is always a good idea. Whether you are visiting the Louvre, climbing the Eiffel Tower, or simply enjoying a croissant at a sidewalk cafe, the City of Light never disappoints. Here is how to make the most of a weekend trip.",
            "pub_date": now - timedelta(days=10),
            "author_id": users[1].id,
            "category_id": categories[1].id,
            "location_id": locations[5].id,
            "is_published": True,
        },
        {
            "title": "Introduction to Machine Learning",
            "text": "Machine learning is transforming industries. From recommendation systems to autonomous vehicles, ML algorithms are everywhere. This post covers the fundamental concepts: supervised learning, unsupervised learning, and reinforcement learning.",
            "pub_date": now - timedelta(days=5),
            "author_id": users[2].id,
            "category_id": categories[0].id,
            "location_id": locations[1].id,
            "is_published": False,
        },
        {
            "title": "The Art of Sourdough Bread",
            "text": "Sourdough bread has a rich history dating back thousands of years. The natural fermentation process gives it a unique tangy flavor and chewy texture. Learn how to create and maintain your own sourdough starter.",
            "pub_date": now - timedelta(days=2),
            "author_id": users[3].id,
            "category_id": categories[2].id,
            "location_id": None,
            "is_published": True,
        },
    ]

    created = []
    for data in posts_data:
        schema = PostCreateSchema(**data)
        async with database.session() as session:
            try:
                post = await repo.create(session=session, data=schema)
                created.append(post)
                logger.info(f"Post created: {post.title} (id={post.id})")
            except Exception as e:
                logger.warning(f"Post {data['title']} skipped: {e}")
    return created


async def seed_comments(users, posts):
    repo = CommentRepository()

    now = datetime.now()
    comments_data = [
        {"text": "Great article! Very helpful for beginners.", "post_id": posts[0].id, "is_published": True},
        {"text": "I have been using FastAPI for a while and it is amazing.", "post_id": posts[0].id, "is_published": True},
        {"text": "Tokyo is my favorite city! Thanks for the tips.", "post_id": posts[1].id, "is_published": True},
        {"text": "I am planning a trip to Japan next year. Saving this!", "post_id": posts[1].id, "is_published": True},
        {"text": "These recipes look delicious. Trying the carbonara tonight!", "post_id": posts[2].id, "is_published": True},
        {"text": "Can you recommend a good pasta machine?", "post_id": posts[2].id, "is_published": False},
        {"text": "Quantum computing is fascinating. Great explanation!", "post_id": posts[3].id, "is_published": True},
        {"text": "Paris in spring is magical. Great itinerary!", "post_id": posts[4].id, "is_published": True},
        {"text": "I would add Montmartre to the list as well.", "post_id": posts[4].id, "is_published": True},
        {"text": "Sourdough is my new obsession. Thanks for the guide!", "post_id": posts[6].id, "is_published": True},
    ]

    created = []
    for i, data in enumerate(comments_data):
        author = users[i % len(users)]
        schema = CommentCreateSchema(**data)
        async with database.session() as session:
            try:
                comment = await repo.create(session=session, data=schema, author_id=author.id)
                created.append(comment)
                logger.info(f"Comment created (id={comment.id}) for post {comment.post_id}")
            except Exception as e:
                logger.warning(f"Comment for post {data['post_id']} skipped: {e}")
    return created


async def seed_post_images(posts):
    image_folder = "/app/images"
    if not os.path.exists(image_folder):
        logger.warning(f"Image folder not found: {image_folder}")
        return []

    repo = PostImageRepository()
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    if not image_files:
        logger.info("No image files found, skipping post images")
        return []

    created = []
    for i, post in enumerate(posts):
        if i < len(image_files):
            img_file = image_files[i]
            create_data = PostImageCreateSchema(
                post_id=post.id,
                file_path=img_file,
                original_name=img_file,
            )
            async with database.session() as session:
                try:
                    post_image = await repo.create(session=session, data=create_data)
                    created.append(post_image)
                    logger.info(f"Post image created: {img_file} for post {post.id}")
                except Exception as e:
                    logger.warning(f"Post image for post {post.id} skipped: {e}")
    return created


async def main(clear_first: bool = True):
    logger.info("Starting seed...")

    if clear_first:
        await clear_data()

    users = await seed_users()
    if not users:
        logger.error("No users created, aborting")
        return

    categories = await seed_categories()
    locations = await seed_locations()
    posts = await seed_posts(users, categories, locations)
    comments = await seed_comments(users, posts)
    post_images = await seed_post_images(posts)

    logger.info("=" * 50)
    logger.info(f"Users:     {len(users)}")
    logger.info(f"Categories: {len(categories)}")
    logger.info(f"Locations:  {len(locations)}")
    logger.info(f"Posts:      {len(posts)}")
    logger.info(f"Comments:   {len(comments)}")
    logger.info(f"Post images: {len(post_images)}")
    logger.info("=" * 50)
    logger.info("Seed completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed database with test data")
    parser.add_argument("--no-clear", action="store_true", help="Do not clear existing data")
    args = parser.parse_args()

    asyncio.run(main(clear_first=not args.no_clear))
