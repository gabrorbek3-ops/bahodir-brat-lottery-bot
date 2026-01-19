import random
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.winner import Winner

class LotteryService:
    @staticmethod
    async def draw_lottery(db: Session, prize: str, youtube_live_id: Optional[str], drawn_by: int):
        approved_orders = db.query(Order).filter(Order.status == "approved").all()
        if not approved_orders:
            raise ValueError("No approved orders available for drawing")

        winner_order = random.choice(approved_orders)
        winner = Winner(
            user_id=winner_order.user_id,
            ticket_id=winner_order.ticket_id,
            prize=prize,
            youtube_live_id=youtube_live_id,
        )
        db.add(winner)
        db.commit()
        db.refresh(winner)

        return {
            "winner_id": winner.id,
            "user_id": winner.user_id,
            "prize": winner.prize,
            "youtube_live_id": winner.youtube_live_id,
            "drawn_at": datetime.utcnow().isoformat(),
            "drawn_by": drawn_by,
        }
