# my_fastapi — Документация проекта

## 📁 Структура проекта

```
my_fastapi/
├── db.sqlite3                      # Основная база данных
├── main.py                         # Точка входа, запуск сервера
├── fill_db.py                      # Скрипт заполнения БД
├── view_db.py                      # Скрипт просмотра БД
├── pyproject.toml                  # Зависимости проекта
└── src/
    ├── app.py                      # Фабрика приложения FastAPI
    ├── api/                        # API роутеры
    │   ├── users.py
    │   ├── posts.py
    │   ├── categories.py
    │   ├── locations.py
    │   └── comments.py
    ├── domain/                     # Бизнес-логика (Use Cases)
    │   ├── user/use_cases/
    │   ├── post/use_cases/
    │   ├── category/use_cases/
    │   ├── location/use_cases/
    │   └── comment/use_cases/
    ├── infrastructure/             # Инфраструктура
    │   └── sqlite/
    │       ├── database.py         # Подключение к БД
    │       ├── models/             # SQLAlchemy модели
    │       └── repositories/       # Репозитории
    └── schemas/                    # Pydantic схемы
```

## 🚀 Быстрый старт

### 1. Запуск сервера
```bash
cd /home/martines/study/back/2/my_fastapi
source venv/bin/activate
python main.py
```

### 2. API доступно по адресу
```
http://localhost:8000/api/v1/
```

### 3. Swagger документация
```
http://localhost:8000/api/v1/docs
```

## 📊 API Endpoints

### Users (Пользователи)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/users/` | Список пользователей |
| GET | `/users/{user_id}` | Получить пользователя по ID |
| POST | `/users/` | Создать пользователя |
| PUT | `/users/{user_id}` | Обновить пользователя |
| DELETE | `/users/{user_id}` | Удалить пользователя |

### Posts (Посты)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/posts/list` | Список всех постов |
| GET | `/posts/get/{post_id}` | Получить пост по ID |
| POST | `/posts/create` | Создать пост |
| PUT | `/posts/update/{post_id}` | Обновить пост |
| DELETE | `/posts/delete/{post_id}` | Удалить пост |

### Categories (Категории)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/categories/list` | Список категорий |
| GET | `/categories/get/{category_id}` | Получить категорию |
| POST | `/categories/create` | Создать категорию |
| PUT | `/categories/update/{category_id}` | Обновить категорию |
| DELETE | `/categories/delete/{category_id}` | Удалить категорию |

### Locations (Местоположения)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/locations/list` | Список местоположений |
| GET | `/locations/get/{location_id}` | Получить местоположение |
| POST | `/locations/create` | Создать местоположение |
| PUT | `/locations/update/{location_id}` | Обновить местоположение |
| DELETE | `/locations/delete/{location_id}` | Удалить местоположение |

### Comments (Комментарии)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/comments/list` | Список комментариев |
| GET | `/comments/list/by_post/{post_id}` | Комментарии к посту |
| GET | `/comments/get/{comment_id}` | Получить комментарий |
| POST | `/comments/create?author_id={id}` | Создать комментарий |
| PUT | `/comments/update/{comment_id}` | Обновить комментарий |
| DELETE | `/comments/delete/{comment_id}` | Удалить комментарий |

## 📝 Примеры запросов

### Создать пользователя
```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "is_active": true
  }'
```

### Создать пост
```bash
curl -X POST http://localhost:8000/api/v1/posts/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Мой пост",
    "text": "Текст поста",
    "pub_date": "2026-03-14T10:00:00",
    "author_id": 1,
    "category_id": 1,
    "is_published": true
  }'
```

### Создать комментарий
```bash
curl -X POST "http://localhost:8000/api/v1/comments/create?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Отличная статья!",
    "post_id": 1,
    "is_published": true
  }'
```

## 🗄 База данных

### Расположение
```
/home/martines/study/back/2/my_fastapi/db.sqlite3
```

### Таблицы
- `auth_user` — пользователи
- `blog_category` — категории
- `blog_location` — местоположения
- `blog_post` — посты
- `blog_comment` — комментарии

### Заполнить БД случайными данными
```bash
cd /home/martines/study/back/2/my_fastapi
source venv/bin/activate
python fill_db.py
```

### Просмотреть БД
```bash
python view_db.py
```

## 🔧 Зависимости

```
fastapi>=0.129.0
pydantic>=2.12.5
uvicorn>=0.41.0
sqlalchemy>=2.0.48
passlib[bcrypt]>=1.7.4
bcrypt>=4.0.1
```

## ✅ Проверки

### Запустить flake8
```bash
source venv/bin/activate
flake8 src/ main.py
```

### Проверить импорты
```bash
python -c "from src.app import create_app; print('OK')"
```

## 📈 Статистика БД (после fill_db.py)

| Сущность | Количество |
|----------|------------|
| Пользователей | 10 |
| Категорий | 4 |
| Местоположений | 5 |
| Постов | 13 |
| Комментариев | 8 |

## 🐛 Исправленные проблемы

1. **Путь к БД** — исправлен в `database.py` (теперь `db.sqlite3` в корне проекта)
2. **Хеширование пароля** — заменён `passlib` на прямой вызов `bcrypt`
3. **CASCADE удаление** — добавлен `cascade='all, delete-orphan'` для комментариев
4. **Загрузка связанных объектов** — добавлен `joinedload` в репозиториях

## 📞 Контакты

Проект: my_fastapi  
Версия: 1.0  
Последнее обновление: 2026-03-14
