import uvicorn

from src.app import create_app
from src.infrastructure.sqlite.database import database

app = create_app()


def run() -> None:
    database.create_tables()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    run()
