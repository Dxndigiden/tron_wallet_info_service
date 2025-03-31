from sqlalchemy import Float, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.core.database import Base


class WalletInfo(Base):
    '''Модель для хранения информации о кошельках.'''

    address: Mapped[str] = mapped_column(
        String(34), unique=True, nullable=False
    )
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False)
    energy: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    last_request_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return (f'<WalletInfo(address={self.address}, balance={self.balance}, '
                f'bandwidth={self.bandwidth}, energy={self.energy})>')
