from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.wallet import (
    WalletRequest,
    WalletResponse,
    WalletInfoResponse,
    WalletListResponse,
)
from app.crud.wallet import create_wallet, get_wallets, count_wallets
from app.services.tron_service import get_wallet_info
from app.core.database import get_db
from app.models.wallet import WalletInfo

router = APIRouter()


@router.get('/')
async def read_root() -> dict[str, str]:
    '''Тестовая ручка для базовой страницы.'''
    return {'message': 'Welcome to TronInfo API!'}


@router.post('/wallet/info', response_model=WalletResponse)
async def get_wallet_info_endpoint(
    wallet_request: Annotated[WalletRequest, Depends()],
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    '''Получает информацию о кошельке и сохраняет её в БД.'''
    wallet_address: str = wallet_request.address

    try:
        wallet_info = await get_wallet_info(wallet_address)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f'Кошелек не найден: {str(e)}'
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Кошелька не существует.'
        )

    existing_wallet = await db.execute(
        select(WalletInfo).filter(WalletInfo.address == wallet_address)
    )
    if existing_wallet.scalars().first() is not None:
        raise HTTPException(
            status_code=400,
            detail='Кошелек уже существует.'
            )

    wallet_record = WalletInfo(
        address=wallet_address,
        balance=wallet_info['balance'],
        bandwidth=wallet_info['bandwidth'],
        energy=wallet_info['energy'],
    )
    await create_wallet(db, wallet_record)

    return WalletResponse(
        address=wallet_address,
        balance=wallet_info['balance'],
        bandwidth=wallet_info['bandwidth'],
        energy=wallet_info['energy'],
    )


@router.get('/wallets', response_model=WalletListResponse)
async def get_wallets_endpoint(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> WalletListResponse:
    '''Получает список кошельков с пагинацией.'''
    wallets = await get_wallets(db, skip, limit)
    total = await count_wallets(db)

    return WalletListResponse(
        wallets=[
            WalletInfoResponse(
                id=wallet.id,
                address=wallet.address,
                balance=wallet.balance,
                bandwidth=wallet.bandwidth,
                energy=wallet.energy,
                created_at=wallet.created_at,
            )
            for wallet in wallets
        ],
        total=total,
    )
