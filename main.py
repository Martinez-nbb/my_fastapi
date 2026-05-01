import asyncio
import uvicorn

from src.app import create_app

app = create_app()


async def run() -> None:
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
    server = uvicorn.Server(config=config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
