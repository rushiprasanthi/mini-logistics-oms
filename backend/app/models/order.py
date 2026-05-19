import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import User


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        Sequence('orders_id_seq'),
        primary_key=True,
        index=True,
    )
    external_id = Column(String(128), unique=True, index=True, nullable=False)
    status = Column(String(32), default=OrderStatus.PENDING.value, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    customer = relationship(User, lazy="joined")
