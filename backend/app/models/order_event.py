from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.db.session import Base


class OrderStatusEvent(Base):
    __tablename__ = "order_status_events"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        index=True,
    )

    from_status = Column(String(32), nullable=False)

    to_status = Column(String(32), nullable=False)

    performed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    reason = Column(String(255), nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
