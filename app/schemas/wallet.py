from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List
import re

# Регулярное выражение для валидации адреса Tron
TRON_ADDRESS_REGEX = r'^T[a-zA-Z0-9]{33}$'


# Схема для запроса информации о кошельке
class WalletRequest(BaseModel):
    address: str = Field(..., max_length=34, description='Адрес кошелька')

    @validator('address')
    def validate_address(cls, value):
        if not re.match(TRON_ADDRESS_REGEX, value):
            raise ValueError('Некорректный адрес кошелька Tron. Адрес должен начинаться с "T" и содержать 34 символа.')
        return value


# Схема для отображения информации о кошельке
class WalletInfoResponse(BaseModel):
    id: int
    address: str
    balance: float
    bandwidth: int
    energy: int
    created_at: datetime
    last_request_at: datetime

    class Config:
        orm_mode = True


# Схема для ответа на запрос списка кошельков с пагинацией
class WalletListResponse(BaseModel):
    total: int
    items: List[WalletInfoResponse]


# Схема для параметров пагинации
class PaginationParams(BaseModel):
    skip: int = Field(0, description='Количество записей, которые нужно пропустить')
    limit: int = Field(10, description='Количество записей для возврата')
