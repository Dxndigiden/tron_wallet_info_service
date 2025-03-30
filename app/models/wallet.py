from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.core.database import Base


# Модель для хранения информации о кошельках
class WalletInfo(Base):
    address: Mapped[str] = mapped_column(String(34), unique=True, nullable=False)  # Адрес кошелька
    balance: Mapped[float] = mapped_column(Float, nullable=False)  # Баланс TRX
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False)  # Bandwidth
    energy: Mapped[int] = mapped_column(Integer, nullable=False)  # Energy
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)  # Время создания записи
    last_request_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)  # Время последнего запроса

    def __repr__(self) -> str:
        return (f"<WalletInfo(address={self.address}, balance={self.balance}, "
                f"bandwidth={self.bandwidth}, energy={self.energy})>")
