#!/bin/sh

# Запуск Alembic миграций
alembic upgrade head

# Заполнение БД тестовыми данными (если переменная SEED_DB=true)
if [ "$SEED_DB" = "true" ]; then
    echo "Seeding database with test data..."
    python -m src.seed
fi

# Запуск приложения
exec python main.py