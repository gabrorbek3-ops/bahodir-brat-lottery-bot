from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, String
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.order import Order
from app.models.winner import Winner
from app.models.payment_card import PaymentCard
from app.schemas.admin import (
    AdminStats, OrderUpdate, CardCreate, 
    LotteryDraw, UserUpdate
)
from app.services.lottery_service import LotteryService
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/admin/stats", response_model=AdminStats)
async def get_admin_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    return await AnalyticsService.get_dashboard_stats(db)

@router.get("/admin/orders")
async def get_orders_admin(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all orders (admin only)"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    total = query.count()
    orders = query.order_by(Order.created_at.desc())\
                 .offset((page - 1) * limit)\
                 .limit(limit)\
                 .all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "orders": orders
    }

@router.put("/admin/orders/{order_id}")
async def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update order status (approve/reject)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already processed"
        )
    
    # Update order
    order.status = order_update.status
    order.admin_notes = order_update.notes
    order.processed_at = datetime.now()
    order.processed_by = current_user.id
    
    # If approved, update user balance
    if order_update.status == "approved":
        user = db.query(User).filter(User.id == order.user_id).first()
        if user:
            user.balance += order.amount
    
    db.commit()
    
    # Send notification to user
    from app.services.notification_service import NotificationService
    await NotificationService.notify_order_status_change(order)
    
    return {"message": f"Order {order_update.status} successfully"}

@router.post("/admin/lottery/draw")
async def draw_lottery(
    lottery_draw: LotteryDraw,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Draw lottery winner"""
    try:
        result = await LotteryService.draw_lottery(
            db=db,
            prize=lottery_draw.prize,
            youtube_live_id=lottery_draw.youtube_live_id,
            drawn_by=current_user.id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/admin/users")
async def get_users(
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all users"""
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (User.first_name.ilike(f"%{search}%")) |
            (User.telegram_id.cast(String).ilike(f"%{search}%"))
        )
    
    if role:
        query = query.filter(User.role == role)
    
    total = query.count()
    users = query.order_by(desc(User.created_at))\
                .offset((page - 1) * limit)\
                .limit(limit)\
                .all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "users": users
    }
