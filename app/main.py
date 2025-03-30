from fastapi import FastAPI

from .core.config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    docs_url='/swagger'
)


@app.get("/")  # Обработчик для корневого маршрута
async def read_root() -> dict:
    """Пробный обработчик маршрута, возвращающий приветственное сообщение."""
    return {"message": "Welcome to TronInfo API!"}