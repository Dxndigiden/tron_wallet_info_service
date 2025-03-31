from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.wallet import WalletInfo


async def create_wallet(
        db: AsyncSession,
        wallet_data: WalletInfo
) -> WalletInfo:
    '''Создает новый кошелек в базе данных.'''
    db.add(wallet_data)
    await db.commit()
    await db.refresh(wallet_data)
    return wallet_data


async def get_wallets(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[WalletInfo]:
    '''Получает список кошельков с пагинацией.'''
    result = await db.execute(
        select(WalletInfo)
        .order_by(WalletInfo.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def count_wallets(db: AsyncSession) -> int:
    '''Считает общее количество кошельков в базе данных.'''
    result = await db.execute(select(WalletInfo))
    return len(result.scalars().all())
