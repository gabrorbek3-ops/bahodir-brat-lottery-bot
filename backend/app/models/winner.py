from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Winner(Base):
    __tablename__ = "winners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prize = Column(String(255), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    youtube_live_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    ticket = relationship("Ticket")

    def __repr__(self) -> str:
        return f"<Winner {self.user_id} ({self.prize})>"
