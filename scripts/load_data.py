import json
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from src.infrastructure.sqlite.database import Database, Base
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.models.post import Post


def load_data():
    db = Database()

    Base.metadata.create_all(bind=db._engine)

    base_dir = Path(__file__).resolve().parent.parent
    json_path = base_dir.parent / 'django_sprint4' / 'db.json'

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with db.session() as session:
        for item in data:
            model = item['model']
            fields = item['fields']
            pk = item['pk']

            if model == 'blog.category':
                category = Category(
                    id=pk,
                    created_at=datetime.fromisoformat(
                        fields['created_at'].replace('Z', '+00:00')
                    ),
                    is_published=fields['is_published'],
                    title=fields['title'],
                    description=fields['description'],
                    slug=fields['slug'],
                )
                session.add(category)

            elif model == 'blog.location':
                location = Location(
                    id=pk,
                    created_at=datetime.fromisoformat(
                        fields['created_at'].replace('Z', '+00:00')
                    ),
                    is_published=fields['is_published'],
                    name=fields['name'],
                )
                session.add(location)

            elif model == 'blog.post':
                post = Post(
                    id=pk,
                    created_at=datetime.fromisoformat(
                        fields['created_at'].replace('Z', '+00:00')
                    ),
                    is_published=fields['is_published'],
                    title=fields['title'],
                    text=fields['text'],
                    pub_date=datetime.fromisoformat(
                        fields['pub_date'].replace('Z', '+00:00')
                    ),
                    author_id=fields['author'],
                    location_id=fields.get('location'),
                    category_id=fields.get('category'),
                    image=fields.get('image', ''),
                )
                session.add(post)

            elif model == 'auth.user':
                user = User(
                    id=pk,
                    password=fields.get('password', ''),
                    is_superuser=fields.get('is_superuser', False),
                    username=fields.get('username', ''),
                    first_name=fields.get('first_name', ''),
                    last_name=fields.get('last_name', ''),
                    email=fields.get('email', ''),
                    is_staff=fields.get('is_staff', False),
                    is_active=fields.get('is_active', True),
                    date_joined=datetime.fromisoformat(
                        fields['date_joined'].replace('Z', '+00:00')
                    )
                    if 'date_joined' in fields
                    else datetime.now(),
                    last_login=datetime.fromisoformat(
                        fields['last_login'].replace('Z', '+00:00')
                    )
                    if fields.get('last_login')
                    else None,
                )
                session.add(user)

        session.commit()

    print('Data loaded successfully!')


if __name__ == '__main__':
    load_data()
