from pydantic import BaseModel
from typing import Optional

class AdminStats(BaseModel):
    total_users: int
    total_orders: int
    total_winners: int
    pending_orders: int
    total_revenue: int

class OrderUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

class CardCreate(BaseModel):
    card_number: str
    bank_name: str
    holder_name: str
    daily_limit: int = 0

class LotteryDraw(BaseModel):
    prize: str
    youtube_live_id: Optional[str] = None

class UserUpdate(BaseModel):
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
