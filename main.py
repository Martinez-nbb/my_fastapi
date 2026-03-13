import asyncio

import uvicorn

from src.app import create_app

from src.infrastructure.sqlite.database import database

app = create_app()

async def run() -> None:

    config = uvicorn.Config(
        app='main:app',

        host='0.0.0.0',

        port=8000,

        reload=False,

        log_level="info",

        access_log=True,
    )

    server = uvicorn.Server(config=config)

    tasks = (asyncio.create_task(server.serve()),)

    # Создаём таблицы (если не существуют)
    database.create_tables()

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    asyncio.run(run())
