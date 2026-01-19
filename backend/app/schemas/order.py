from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    ticket_id: int
    screenshot_data: Optional[str] = None

class OrderUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    ticket_id: int
    amount: int
    status: str
    screenshot_url: Optional[str] = None
    screenshot_data: Optional[str] = None
    admin_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    processed_by: Optional[int] = None

    class Config:
        orm_mode = True
