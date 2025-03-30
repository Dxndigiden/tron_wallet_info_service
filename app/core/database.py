from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker, Mapped, mapped_column

from app.core.config import settings


# Базовый класс для моделей
class PreBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


# Базовый класс для SQLAlchemy
Base = declarative_base(cls=PreBase)

# Создание асинхронного движка базы данных
engine = create_async_engine(settings.database_url, echo=True)

# Создание локальной асинхронной сессии
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
