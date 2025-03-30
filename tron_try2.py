import asyncio

from decouple import config
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound


WALLET_ADDRESS = config('WALLET_ADDRESS')
API_KEY = config('API_KEY')


async def get_wallet_info(wallet_address, api_key):
    # Создаем экземпляр асинхронного клиента Tron с API-ключом
    client = AsyncTron(AsyncHTTPProvider(api_key=api_key))

    try:
        # Получаем информацию о кошельке
        account_info = await client.get_account(wallet_address)
        bandwidth = await client.get_bandwidth(wallet_address)
        account_resource = await client.get_account_resource(wallet_address)

        # Извлекаем баланс
        balance = account_info.get('balance', 0)  # Баланс в SUN
        balance_trx = balance / 1_000_000

        # Извлекаем доступные значения для энергии
        energy = account_resource.get('EnergyLimit', 0) - account_resource.get('EnergyUsed', 0)

        # Вывод информации о балансе, пропускной способности и энергии
        print(f'Баланс TRX для адреса {wallet_address}: {balance_trx:.6f} TRX')
        print(f'Bandwidth: {bandwidth}' )
        print(f'Energy: {energy}')

    except AddressNotFound:
        print(f'Адрес {wallet_address} не найден в блокчейне.')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

# Пример использования
if __name__ == '__main__':
    wallet_address = WALLET_ADDRESS
    api_key = API_KEY
    asyncio.run(get_wallet_info(wallet_address, api_key))
