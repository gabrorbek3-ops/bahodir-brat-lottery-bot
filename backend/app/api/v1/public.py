from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.ticket import Ticket
from app.models.payment_card import PaymentCard
from app.models.winner import Winner
from app.models.user import User
from app.schemas.public import (
    TicketResponse,
    PaymentCardResponse,
    WinnerResponse,
    TelegramUserCreate,
    TelegramUserResponse,
)

router = APIRouter()

@router.get("/tickets", response_model=List[TicketResponse])
async def get_tickets(db: Session = Depends(get_db)):
    """Get active tickets for purchase."""
    tickets = db.query(Ticket).filter(Ticket.is_active == True).all()
    return tickets

@router.get("/payment-card", response_model=PaymentCardResponse)
async def get_payment_card(db: Session = Depends(get_db)):
    """Get active payment card details."""
    card = (
        db.query(PaymentCard)
        .filter(PaymentCard.is_active == True)
        .order_by(PaymentCard.created_at.desc())
        .first()
    )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment card not found",
        )
    return card

@router.get("/winners", response_model=List[WinnerResponse])
async def get_winners(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent winners."""
    winners = (
        db.query(Winner)
        .order_by(Winner.created_at.desc())
        .limit(limit)
        .all()
    )
    response = []
    for winner in winners:
        user_name = winner.user.full_name if winner.user else None
        response.append(
            WinnerResponse(
                id=winner.id,
                user_id=winner.user_id,
                prize=winner.prize,
                user_name=user_name,
                ticket_id=winner.ticket_id,
                youtube_live_id=winner.youtube_live_id,
                created_at=winner.created_at,
            )
        )
    return response

@router.post("/users/telegram", response_model=TelegramUserResponse)
async def upsert_telegram_user(
    payload: TelegramUserCreate,
    db: Session = Depends(get_db),
):
    """Create or update a user from Telegram account data."""
    user = db.query(User).filter(User.telegram_id == payload.telegram_id).first()
    if not user:
        user = User(
            telegram_id=payload.telegram_id,
            username=payload.username,
            first_name=payload.first_name,
            last_name=payload.last_name,
            language_code=payload.language_code,
        )
        db.add(user)
    else:
        user.username = payload.username or user.username
        user.first_name = payload.first_name or user.first_name
        user.last_name = payload.last_name or user.last_name
        user.language_code = payload.language_code or user.language_code
    db.commit()
    return TelegramUserResponse(status="ok", user_id=user.id)
