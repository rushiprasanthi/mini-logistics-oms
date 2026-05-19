from typing import Optional

from sqlalchemy.orm import Session

from app.repositories.audit_repo import AuditRepository


class AuditService:
    def __init__(self, db: Session):
        self.repo = AuditRepository(db)

    def record_order_transition(
        self,
        order_id: int,
        from_status: str,
        to_status: str,
        performed_by: Optional[int] = None,
        reason: Optional[str] = None,
    ):
        return self.repo.create_event(
            order_id=order_id,
            from_status=from_status,
            to_status=to_status,
            performed_by=performed_by,
            reason=reason,
        )
