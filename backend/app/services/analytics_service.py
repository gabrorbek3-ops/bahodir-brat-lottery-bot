from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.order import Order
from app.models.winner import Winner
from app.schemas.admin import AdminStats

class AnalyticsService:
    @staticmethod
    async def get_dashboard_stats(db: Session) -> AdminStats:
        total_users = db.query(func.count(User.id)).scalar() or 0
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        total_winners = db.query(func.count(Winner.id)).scalar() or 0
        pending_orders = (
            db.query(func.count(Order.id))
            .filter(Order.status == "pending")
            .scalar()
            or 0
        )
        total_revenue = (
            db.query(func.coalesce(func.sum(Order.amount), 0))
            .filter(Order.status == "approved")
            .scalar()
            or 0
        )
        return AdminStats(
            total_users=total_users,
            total_orders=total_orders,
            total_winners=total_winners,
            pending_orders=pending_orders,
            total_revenue=total_revenue,
        )
