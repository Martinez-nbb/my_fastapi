#!/bin/sh

export DATABASE_URL
alembic upgrade head
exec python main.py
