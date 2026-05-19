from sqlalchemy.orm import Session

from app.models.order_event import OrderStatusEvent


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(
        self,
        order_id: int,
        from_status: str,
        to_status: str,
        performed_by: int = None,
        reason: str = None,
    ):
        event = OrderStatusEvent(
            order_id=order_id,
            from_status=from_status,
            to_status=to_status,
            performed_by=performed_by,
            reason=reason,
        )

        self.db.add(event)

        # Service layer handles commit/rollback
        self.db.flush()
        self.db.refresh(event)

        return event
