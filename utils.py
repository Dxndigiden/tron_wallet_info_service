import asyncio

from decouple import config
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound


# Получаем адрес кошелька и API-ключ из переменных окружения
WALLET_ADDRESS: str = config('WALLET_ADDRESS')
API_KEY: str = config('API_KEY')


async def get_wallet_info(wallet_address: str, api_key: str) -> None:
    """
    Получает информацию о кошельке, включая баланс, пропускную способность и энергию.

    :param wallet_address: Адрес кошелька в сети Tron.
    :param api_key: API-ключ для доступа к Tron API.
    """
    # Создаем экземпляр асинхронного клиента Tron с API-ключом
    client = AsyncTron(AsyncHTTPProvider(api_key=api_key))

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

        # Вывод информации о балансе, пропускной способности и энергии
        print(f'Баланс TRX для адреса {wallet_address}: {balance_trx:.6f} TRX')
        print(f'Пропускная способность: {bandwidth}')
        print(f'Энергия: {energy}')

    except AddressNotFound:
        print(f'Адрес {wallet_address} не найден в блокчейне.')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


# Пример использования
if __name__ == '__main__':
    wallet_address: str = WALLET_ADDRESS
    api_key: str = API_KEY
    asyncio.run(get_wallet_info(wallet_address, api_key))
