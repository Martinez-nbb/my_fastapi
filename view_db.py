import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'db.sqlite3'


def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    print(f"\n{'='*60}")
    print(f"Таблица: {table_name} ({len(rows)} записей)")
    print(f"{'='*60}")
    print(" | ".join(columns))
    print("-" * 60)

    for row in rows[:10]:
        print(" | ".join(str(v) for v in row))

    if len(rows) > 10:
        print(f"... и ещё {len(rows) - 10} записей")


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        'auth_user', 'blog_category', 'blog_location',
        'blog_post', 'blog_comment'
    ]

    for table in tables:
        print_table(cursor, table)

    conn.close()


if __name__ == '__main__':
    main()
