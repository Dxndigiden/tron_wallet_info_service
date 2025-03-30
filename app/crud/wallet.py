from datetime import datetime

from sqlalchemy.orm import Session

from app.models.wallet import WalletInfo
from app.schemas.wallet import WalletRequest, WalletInfoResponse, WalletListResponse, PaginationParams
from app.services.tron_service import get_wallet_info


# Функция для создания или обновления информации о кошельке
async def create_or_update_wallet_info(db: Session, wallet_request: WalletRequest) -> WalletInfoResponse:
    # Получаем информацию о кошельке из Tron
    wallet_info = await get_wallet_info(wallet_request.address)

    # Проверяем, существует ли запись о кошельке
    wallet_record = db.query(WalletInfo).filter(WalletInfo.address == wallet_request.address).first()

    if wallet_record:
        # Обновляем существующую запись
        wallet_record.balance = wallet_info['balance']
        wallet_record.bandwidth = wallet_info['bandwidth']
        wallet_record.energy = wallet_info['energy']
        wallet_record.last_request_at = datetime.utcnow()
    else:
        # Создаем новую запись
        wallet_record = WalletInfo(
            address=wallet_request.address,
            balance=wallet_info['balance'],
            bandwidth=wallet_info['bandwidth'],
            energy=wallet_info['energy'],
            created_at=datetime.utcnow(),
            last_request_at=datetime.utcnow()
        )
        db.add(wallet_record)

    db.commit()
    db.refresh(wallet_record)

    return WalletInfoResponse(
        id=wallet_record.id,
        address=wallet_record.address,
        balance=wallet_record.balance,
        bandwidth=wallet_record.bandwidth,
        energy=wallet_record.energy,
        created_at=wallet_record.created_at,
        last_request_at=wallet_record.last_request_at
    )


# Функция для получения списка кошельков с пагинацией
def get_wallets(db: Session, pagination: PaginationParams) -> WalletListResponse:
    total = db.query(WalletInfo).count()
    items = db.query(WalletInfo).order_by(WalletInfo.created_at.desc()).offset(pagination.skip).limit(pagination.limit).all()

    return WalletListResponse(
        total=total,
        items=[WalletInfoResponse(
            id=wallet.id,
            address=wallet.address,
            balance=wallet.balance,
            bandwidth=wallet.bandwidth,
            energy=wallet.energy,
            created_at=wallet.created_at,
            last_request_at=wallet.last_request_at
        ) for wallet in items]
    )
