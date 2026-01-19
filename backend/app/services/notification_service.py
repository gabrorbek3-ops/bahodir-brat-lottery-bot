import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    async def notify_new_order(order, user):
        logger.info("New order %s from user %s", order.id, user.id)

    @staticmethod
    async def notify_receipt_uploaded(order, user):
        logger.info("Receipt uploaded for order %s by user %s", order.id, user.id)

    @staticmethod
    async def notify_order_status_change(order):
        logger.info("Order %s status changed to %s", order.id, order.status)
