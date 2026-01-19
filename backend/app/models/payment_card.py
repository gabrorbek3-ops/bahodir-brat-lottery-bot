from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

class PaymentCard(Base):
    __tablename__ = "payment_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(32), nullable=False)
    bank_name = Column(String(255), nullable=False)
    holder_name = Column(String(255), nullable=False)
    daily_limit = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<PaymentCard {self.bank_name} ({self.card_number})>"
