import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.main import app
from app.core.database import AsyncSessionLocal
from app.models.wallet import WalletInfo


@pytest_asyncio.fixture(scope='function')
async def db_session() -> AsyncSession:
    """Создает новую асинхронную сессию базы данных для тестов."""
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope='function')
def client() -> TestClient:
    """Создает экземпляр клиента FastAPI для тестирования."""
    return TestClient(app)


async def delete_wallet_if_exists(
        db_session: AsyncSession,
        wallet_address: str
):
    """Удаляет кошелек из базы данных, если он существует."""
    existing_wallet = await db_session.execute(
        select(WalletInfo).filter(WalletInfo.address == wallet_address)
    )
    existing_wallet = existing_wallet.scalars().first()
    if existing_wallet:
        await db_session.delete(existing_wallet)
        await db_session.commit()


@pytest.mark.asyncio
async def test_wallet_info(
    client: TestClient,
    db_session: AsyncSession
) -> None:
    """Интеграционный тест для получения информации о кошельке
    и проверки обработки некорректного адреса.
    """
    wallet_address = 'TYEMUMKBmkTRMa1CNh7xkNYZ2mTVFw9f1a'

    await delete_wallet_if_exists(db_session, wallet_address)

    response = client.post(
        '/api/wallet/info?address=' + wallet_address,
        json={'address': wallet_address}
    )

    assert response.status_code == 200
    data = response.json()
    assert data['address'] == wallet_address
    assert 'balance' in data
    assert 'bandwidth' in data
    assert 'energy' in data

    created_wallet = await db_session.execute(
        select(WalletInfo).filter(WalletInfo.address == wallet_address)
    )

    created_wallet = created_wallet.scalars().first()
    assert created_wallet is not None

    await db_session.delete(created_wallet)
    await db_session.commit()

    wallet_record_after_delete = await db_session.execute(
        select(WalletInfo).filter(WalletInfo.address == wallet_address)
    )

    assert wallet_record_after_delete.scalars().first() is None

    invalid_address = 'INVALID_ADDRESS'
    response = client.post(
        '/api/wallet/info?address=' + invalid_address,
        json={'address': invalid_address}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_wallet(db_session: AsyncSession) -> None:
    """Юнит-тест для создания нового кошелька в базе данных."""

    wallet_address = 'TYEMUMKBmkTRMa1CNh7xkNYZ2mTVFw9f1a'

    await delete_wallet_if_exists(db_session, wallet_address)

    wallet_info = {
        'balance': 666.0,
        'bandwidth': 600,
        'energy': 1337,
    }

    wallet_record = WalletInfo(
        address=wallet_address,
        balance=wallet_info['balance'],
        bandwidth=wallet_info['bandwidth'],
        energy=wallet_info['energy'],
    )

    db_session.add(wallet_record)
    await db_session.commit()

    await db_session.refresh(wallet_record)

    assert wallet_record.address == wallet_address
    assert wallet_record.balance == wallet_info['balance']
    assert wallet_record.bandwidth == wallet_info['bandwidth']
    assert wallet_record.energy == wallet_info['energy']

    await db_session.delete(wallet_record)
    await db_session.commit()
