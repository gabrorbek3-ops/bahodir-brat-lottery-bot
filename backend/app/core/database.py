from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency for getting database session
def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db() -> None:
    """Initialize database with sample data"""
    from app.models.user import User
    from app.models.ticket import Ticket
    from app.models.payment_card import PaymentCard
    
    db = SessionLocal()
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Check if tickets exist
        if not db.query(Ticket).first():
            tickets = [
                Ticket(
                    name="Oddiy Bilet",
                    price=500,
                    description="1x imkoniyat",
                    multiplier=1
                ),
                Ticket(
                    name="Oltin Bilet",
                    price=1000,
                    description="3x imkoniyat",
                    multiplier=3
                ),
                Ticket(
                    name="VIP Bilet",
                    price=5000,
                    description="10x imkoniyat",
                    multiplier=10
                )
            ]
            db.add_all(tickets)
            
        # Check if payment cards exist
        if not db.query(PaymentCard).first():
            card = PaymentCard(
                card_number="2202 2020 4444 5555",
                bank_name="Sberbank",
                holder_name="BAHODIR B.",
                daily_limit=100000,
                is_active=True
            )
            db.add(card)
        
        db.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        db.rollback()
    finally:
        db.close()
