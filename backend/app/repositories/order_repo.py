from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id: int) -> Optional[Order]:
        return (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    def get_by_external_id(self, external_id: str) -> Optional[Order]:
        return (
            self.db.query(Order)
            .filter(Order.external_id == external_id)
            .first()
        )

    def create(
        self,
        external_id: str,
        customer_id: Optional[int] = None,
    ) -> Order:
        order = Order(
            external_id=external_id.strip(),
            customer_id=customer_id,
        )

        self.db.add(order)

        # IMPORTANT:
        # do NOT commit in repository
        # service layer controls transaction lifecycle
        self.db.flush()
        self.db.refresh(order)

        return order

    def update_status(
        self,
        order: Order,
        status,
    ) -> Order:
        order.status = (
            status.value
            if hasattr(status, "value")
            else str(status)
        )

        self.db.add(order)

        # IMPORTANT:
        # service layer handles commit/rollback
        self.db.flush()
        self.db.refresh(order)

        return order

    def list_for_owner(
        self,
        owner_id: int,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ):
        query = (
            self.db.query(Order)
            .filter(Order.customer_id == owner_id)
        )

        if status:
            query = query.filter(Order.status == status)

        total = query.count()

        items = (
            query.order_by(Order.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return items, total

    def list_all(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ):
        query = self.db.query(Order)

        if status:
            query = query.filter(Order.status == status)

        if search:
            query = query.filter(
                func.lower(Order.external_id).like(
                    f"%{search.lower()}%"
                )
            )

        total = query.count()

        items = (
            query.order_by(Order.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return items, total
