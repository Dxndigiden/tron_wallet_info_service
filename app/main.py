from fastapi import FastAPI
from app.core.config import settings
from app.api.router import router

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    docs_url='/swagger'
)


# Интеграция роутера
app.include_router(router)
