from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketResponse(BaseModel):
    id: int
    name: str
    price: int
    description: Optional[str] = None
    multiplier: int

    class Config:
        orm_mode = True

class PaymentCardResponse(BaseModel):
    id: int
    card_number: str
    bank_name: str
    holder_name: str
    daily_limit: int

    class Config:
        orm_mode = True

class WinnerResponse(BaseModel):
    id: int
    user_id: int
    prize: str
    user_name: Optional[str] = None
    ticket_id: Optional[int] = None
    youtube_live_id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TelegramUserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None

class TelegramUserResponse(BaseModel):
    status: str
    user_id: int
