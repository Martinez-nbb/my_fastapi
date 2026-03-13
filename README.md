# my_fastapi — Блог-платформа на FastAPI

REST API для блога, реализованное на FastAPI с использованием SQLAlchemy и SQLite.

## Архитектура проекта

Проект использует архитектуру, аналогичную `backend-fastapi-task1`:

```
src/
├── api/                      # Слой маршрутизации (контроллеры)
│   ├── users.py
│   ├── categories.py
│   ├── locations.py
│   ├── posts.py
│   └── comments.py
├── domain/                   # Бизнес-логика (use cases)
│   ├── user/use_cases/
│   ├── category/use_cases/
│   ├── location/use_cases/
│   ├── post/use_cases/
│   └── comment/use_cases/
├── infrastructure/           # Инфраструктурный слой (БД, репозитории)
│   └── sqlite/
│       ├── database.py
│       ├── metadata.py
│       ├── models/
│       └── repositories/
├── schemas/                  # Pydantic-схемы (DTO)
└── app.py                   # Фабрика приложения
```

## Сущности

- **User** — пользователь (таблица: `auth_user`)
- **Category** — категория публикаций (таблица: `blog_category`)
- **Location** — местоположение (таблица: `blog_location`)
- **Post** — публикация (таблица: `blog_post`)
- **Comment** — комментарий (таблица: `blog_comment`)

## Установка и запуск

### 1. Установка зависимостей

```bash
cd my_fastapi
source venv/bin/activate
pip install -r requirements.txt  # или используйте pyproject.toml
```

### 2. Подключение базы данных Django

Для использования базы данных из Django приложения:

1. Убедитесь, что файл `db.sqlite3` существует в директории `django_sprint4/`
2. В файле `src/infrastructure/sqlite/database.py` раскомментируйте строки:
   ```python
   base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
   db_path = base_dir / 'django_sprint4' / 'db.sqlite3'
   ```
3. Закомментируйте временную БД:
   ```python
   # base_dir = Path(__file__).resolve().parent.parent.parent.parent
   # db_path = base_dir / 'db.sqlite3'
   ```

### 3. Создание таблиц

При первом запуске таблицы создаются автоматически:

```bash
python main.py
```

### 4. Запуск сервера

```bash
python main.py
```

Сервер запустится на `http://0.0.0.0:8000`

## API Endpoints

### Health Check
- `GET /api/v1/health` — проверка работоспособности

### Users
- `GET /api/v1/users/` — список всех пользователей
- `GET /api/v1/users/{user_id}` — получить пользователя по ID
- `POST /api/v1/users/` — создать пользователя
- `PUT /api/v1/users/{user_id}` — обновить пользователя
- `DELETE /api/v1/users/{user_id}` — удалить пользователя

### Categories
- `GET /api/v1/categories/list` — список всех категорий
- `GET /api/v1/categories/get/{category_id}` — получить категорию по ID
- `POST /api/v1/categories/create` — создать категорию
- `PUT /api/v1/categories/update/{category_id}` — обновить категорию
- `DELETE /api/v1/categories/delete/{category_id}` — удалить категорию

### Locations
- `GET /api/v1/locations/list` — список всех местоположений
- `GET /api/v1/locations/get/{location_id}` — получить местоположение по ID
- `POST /api/v1/locations/create` — создать местоположение
- `PUT /api/v1/locations/update/{location_id}` — обновить местоположение
- `DELETE /api/v1/locations/delete/{location_id}` — удалить местоположение

### Posts
- `GET /api/v1/posts/list` — список всех публикаций
- `GET /api/v1/posts/get/{post_id}` — получить публикацию по ID
- `POST /api/v1/posts/create` — создать публикацию
- `PUT /api/v1/posts/update/{post_id}` — обновить публикацию
- `DELETE /api/v1/posts/delete/{post_id}` — удалить публикацию

### Comments
- `GET /api/v1/comments/list` — список всех комментариев
- `GET /api/v1/comments/list/by_post/{post_id}` — комментарии к публикации
- `GET /api/v1/comments/get/{comment_id}` — получить комментарий по ID
- `POST /api/v1/comments/create` — создать комментарий
- `PUT /api/v1/comments/update/{comment_id}` — обновить комментарий
- `DELETE /api/v1/comments/delete/{comment_id}` — удалить комментарий

## Документация API

После запуска сервера документация доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Структура базы данных

### Таблица `auth_user`
- `id` — первичный ключ
- `username` — имя пользователя (уникальное)
- `password` — хеш пароля
- `email` — email
- `is_active` — активен ли пользователь
- `is_superuser` — является ли суперпользователем
- `is_staff` — является ли сотрудником
- `date_joined` — дата регистрации

### Таблица `blog_category`
- `id` — первичный ключ
- `title` — заголовок категории
- `description` — описание
- `slug` — URL-идентификатор
- `is_published` — опубликовано
- `created_at` — дата создания

### Таблица `blog_location`
- `id` — первичный ключ
- `name` — название места
- `is_published` — опубликовано
- `created_at` — дата создания

### Таблица `blog_post`
- `id` — первичный ключ
- `title` — заголовок
- `text` — текст публикации
- `pub_date` — дата публикации
- `author_id` — ID автора (внешний ключ на `auth_user`)
- `location_id` — ID местоположения (внешний ключ на `blog_location`, nullable)
- `category_id` — ID категории (внешний ключ на `blog_category`, nullable)
- `image` — путь к изображению
- `is_published` — опубликовано
- `created_at` — дата создания

### Таблица `blog_comment`
- `id` — первичный ключ
- `text` — текст комментария
- `post_id` — ID публикации (внешний ключ на `blog_post`)
- `author_id` — ID автора (внешний ключ на `auth_user`)
- `is_published` — опубликовано
- `created_at` — дата создания

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM
- **Pydantic** — валидация данных
- **SQLite** — база данных
- **Uvicorn** — ASGI-сервер
