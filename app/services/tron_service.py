
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound

from app.core.config import settings

# Получаем API-ключ из переменных окружения
API_KEY: str = settings.api_key


async def get_wallet_info(wallet_address: str) -> dict:
    """
    Получает информацию о кошельке, включая баланс, bandwidth(пропускную способность) и энергию.

    :param wallet_address: Адрес кошелька в сети Tron.
    :return: Словарь с информацией о кошельке.
    """
    # Создаем экземпляр асинхронного клиента Tron с API-ключом
    client = AsyncTron(AsyncHTTPProvider(api_key=API_KEY))

    try:
        # Получаем информацию о кошельке
        account_info = await client.get_account(wallet_address)
        bandwidth = await client.get_bandwidth(wallet_address)
        account_resource = await client.get_account_resource(wallet_address)

        # Извлекаем баланс
        balance: int = account_info.get('balance', 0)  # Баланс в SUN
        balance_trx: float = balance / 1_000_000

        # Извлекаем доступные значения для энергии
        energy: int = account_resource.get('EnergyLimit', 0) - account_resource.get('EnergyUsed', 0)

        return {
            'balance': balance_trx,
            'bandwidth': bandwidth,
            'energy': energy
        }

    except AddressNotFound:
        raise ValueError(f'Адрес {wallet_address} не найден в блокчейне.')
    except Exception as e:
        raise Exception(f'Произошла ошибка: {e}')
