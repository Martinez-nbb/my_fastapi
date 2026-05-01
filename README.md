# MyFastAPI

FastAPI блог-платформа с использованием PostgreSQL, Alembic и логированием.

## Требования

- Python 3.12+
- PostgreSQL (или SQLite для разработки)
- Docker и Docker Compose (для контейнеризации)

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd my_fastapi
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Отредактируйте `.env` под ваши настройки.

5. Запустите миграции:
```bash
alembic upgrade head
```

6. Запустите приложение:
```bash
python main.py
```

### Запуск через Docker

1. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

2. Отредактируйте `.env`, установив DATABASE_URL для PostgreSQL:
```
DATABASE_URL=postgresql+psycopg2://user:password@db:5432/myfastapi
```

3. Запустите через Docker Compose:
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000/api/v1

## Функциональность

- Аутентификация пользователей (JWT)
- CRUD операции для пользователей, постов, категорий, локаций, комментариев
- Автоматические миграции через Alembic
- Логирование действий пользователей
- Настройки через переменные окружения (Pydantic-Settings)

## Переменные окружения

См. файл `.env.example` для списка доступных переменных.

## Структура проекта

```
my_fastapi/
├── src/
│   ├── api/          # Маршруты API
│   ├── core/         # Конфигурация, логирование
│   ├── domain/       # Бизнес-логика (use cases)
│   ├── infrastructure/ # Работа с БД
│   ├── schemas/      # Pydantic схемы
│   └── resources/    # Вспомогательные ресурсы
├── alembic/          # Миграции
├── logs/             # Логи приложения
├── main.py           # Точка входа
├── requirements.txt  # Зависимости
└── docker-compose.yml
```

## Логирование

Логи сохраняются в папку `logs/` с именем `app_YYYYMMDD.log` и выводятся в консоль.
