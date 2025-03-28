from tronpy import Tron
import time

# Инициализация клиента
client = Tron()

addresses = [
    'TPqmGMoidNTbMZ8ApgcbPMf7JDyiHi1sv5',
    'TGfWKtSDs96TrX1GwH3xsf5HxZhj1PPydv',
]


def format_response(address, balance, bandwidth, energy):
    print(f'Адрес: {address}')
    print(f'Баланс TRX: {balance} TRX')
    print(f'Доступный bandwidth: {bandwidth} (в байтах)')
    print(f'Доступная энергия: {energy} (в единицах)')
    print('-' * 40)


for address in addresses:
    try:
        account_info = client.get_account(address)
        balance = account_info['balance']

        # Проверка наличия ресурсов
        account_resource = account_info.get('account_resource', {})
        bandwidth = account_resource.get('bandwidth', 'Информация недоступна')
        energy = account_resource.get('energy', 'Информация недоступна')

        format_response(address, balance, bandwidth, energy)
        time.sleep(2)
    except Exception as e:
        print(f'Ошибка при получении информации для адреса {address}: {e}')
        time.sleep(2)
