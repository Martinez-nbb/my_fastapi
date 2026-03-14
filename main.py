import asyncio

import uvicorn

from src.app import create_app
from src.infrastructure.sqlite.database import database

app = create_app()


async def run() -> None:
    config = uvicorn.Config(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
    server = uvicorn.Server(config=config)
    tasks = (asyncio.create_task(server.serve()),)

    database.create_tables()

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    asyncio.run(run())
