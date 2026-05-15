#!/bin/sh

# Запуск Alembic миграций
alembic upgrade head

# Запуск приложения
exec python main.py