from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    screenshot_url = Column(Text, nullable=True)
    screenshot_data = Column(Text, nullable=True)  # base64 encoded
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    ticket = relationship("Ticket")
    processor = relationship("User", foreign_keys=[processed_by])
    
    def __repr__(self):
        return f"<Order {self.id} ({self.status})>"
