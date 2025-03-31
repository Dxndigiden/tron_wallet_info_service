from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    Mapped,
    mapped_column
)

from app.core.config import settings


class PreBase:
    '''Базовый класс для моделей.'''
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


# Базовый класс для SQLAlchemy
Base = declarative_base(cls=PreBase)

# Создание асинхронного движка базы данных
engine = create_async_engine(settings.database_url, echo=True)

# Создание локальной асинхронной сессии
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    '''Возвращает асинхронную сессию базы данных.'''
    async with AsyncSessionLocal() as session:
        yield session
