from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = 'TronInfo'
    description: str = 'Tron Wallet Info Service'
    api_key: str = config('API_KEY')  # API ключ для Tron
    database_url: str = 'sqlite+aiosqlite:///./tronwallet.db'

    class Config:
        """Конфигурация Pydantic для загрузки переменных окружения."""
        env_file = '.env'


settings = Settings()