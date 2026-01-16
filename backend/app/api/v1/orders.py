from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import base64
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.order import Order
from app.models.ticket import Ticket
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.utils.image_processor import ImageProcessor

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new order (purchase ticket)"""
    
    # Check if ticket exists
    ticket = db.query(Ticket).filter(
        Ticket.id == order_data.ticket_id,
        Ticket.is_active == True
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Process image if provided
    screenshot_data = None
    if order_data.screenshot_data:
        try:
            # Validate and process image
            screenshot_data = await ImageProcessor.validate_and_process(
                order_data.screenshot_data
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Create order
    order = Order(
        user_id=current_user.id,
        ticket_id=ticket.id,
        amount=ticket.price,
        screenshot_data=screenshot_data,
        status="pending"
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Send notification to admins
    await NotificationService.notify_new_order(order, current_user)
    
    return order

@router.get("/orders/my", response_model=List[OrderResponse])
async def get_my_orders(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's orders"""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).all()
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permission
    if order.user_id != current_user.id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    return order

@router.post("/orders/upload-receipt")
async def upload_receipt(
    order_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload receipt for existing order"""
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,
        Order.status == "pending"
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or not pending"
        )
    
    # Validate file
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )
    
    # Read and process image
    contents = await file.read()
    
    if len(contents) > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 5MB)"
        )
    
    # Convert to base64
    screenshot_data = f"data:{file.content_type};base64,{base64.b64encode(contents).decode()}"
    
    # Update order
    order.screenshot_data = screenshot_data
    db.commit()
    
    # Notify admins
    await NotificationService.notify_receipt_uploaded(order, current_user)
    
    return {"message": "Receipt uploaded successfully"}
