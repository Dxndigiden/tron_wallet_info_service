from pydantic import BaseModel, Field
from datetime import datetime


class WalletRequest(BaseModel):
    '''Запрос на получение информации о кошельке.'''
    address: str = Field(
        ...,
        pattern=r'^T[a-zA-Z0-9]{33}$',
        description=(
            'Адрес кошелька в сети Tron, должен начинаться с '
            '"T" и содержать 34 символа.'
        )
    )


class WalletResponse(BaseModel):
    '''Ответ с информацией о кошельке.'''
    address: str
    balance: float
    bandwidth: int
    energy: int


class WalletInfoResponse(BaseModel):
    '''Ответ с детальной информацией о кошельке.'''
    id: int
    address: str
    balance: float
    bandwidth: int
    energy: int
    created_at: datetime


class WalletListResponse(BaseModel):
    '''Ответ со списком кошельков.'''
    wallets: list[WalletInfoResponse]
    total: int
