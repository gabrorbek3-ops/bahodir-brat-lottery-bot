from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.user import User

async def get_current_user(
    x_telegram_id: Optional[int] = Header(default=None, alias="X-Telegram-Id"),
    x_username: Optional[str] = Header(default=None, alias="X-Username"),
    x_first_name: Optional[str] = Header(default=None, alias="X-First-Name"),
    x_last_name: Optional[str] = Header(default=None, alias="X-Last-Name"),
    db: Session = Depends(get_db),
) -> User:
    if not x_telegram_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telegram account header missing",
        )

    user = db.query(User).filter(User.telegram_id == x_telegram_id).first()
    if not user:
        user = User(
            telegram_id=x_telegram_id,
            username=x_username,
            first_name=x_first_name,
            last_name=x_last_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in {"admin", "superadmin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
