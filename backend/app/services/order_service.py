from typing import List, Optional, Tuple
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateError,
    ForbiddenError,
    InvalidTransitionError,
    NotFoundError,
    ValidationError,
)
from app.models.order import Order, OrderStatus
from app.repositories.order_repo import OrderRepository
from app.repositories.user_repo import UserRepository
from app.services.audit_service import AuditService


logger = logging.getLogger(__name__)


class OrderService:
    """
    Service layer for OMS order operations.

    Handles:
    - FSM workflow validation
    - RBAC validation
    - transaction orchestration
    - audit orchestration
    """

    ALLOWED_TRANSITIONS = {
        OrderStatus.PENDING: [
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED,
        ],
        OrderStatus.CONFIRMED: [
            OrderStatus.SHIPPED,
            OrderStatus.CANCELLED,
        ],
        OrderStatus.SHIPPED: [
            OrderStatus.DELIVERED,
        ],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)
        self.user_repo = UserRepository(db)
        self.audit = AuditService(db)

    def create_order(
        self,
        external_id: str,
        customer_id: Optional[int] = None,
    ) -> Order:
        external_id = external_id.strip()

        if not external_id:
            raise ValidationError(
                "external_id cannot be empty",
                code="EMPTY_EXTERNAL_ID",
            )

        if len(external_id) > 128:
            raise ValidationError(
                "external_id too long",
                code="EXTERNAL_ID_TOO_LONG",
            )

        if customer_id:
            customer = self.user_repo.get(customer_id)

            if not customer:
                raise NotFoundError(
                    f"customer {customer_id} not found",
                    code="CUSTOMER_NOT_FOUND",
                )

        try:
            order = self.repo.create(
                external_id=external_id,
                customer_id=customer_id,
            )

            self.db.commit()
            self.db.refresh(order)

            logger.info(
                f"Order created: "
                f"{external_id} "
                f"(id={order.id})"
            )

            return order

        except IntegrityError:
            self.db.rollback()

            logger.warning(
                f"Duplicate external_id: {external_id}"
            )

            raise DuplicateError(
                f"external_id '{external_id}' already exists",
                code="DUPLICATE_EXTERNAL_ID",
            )

    def get_order(
        self,
        external_id: str,
    ) -> Order:
        order = self.repo.get_by_external_id(
            external_id.strip()
        )

        if not order:
            raise NotFoundError(
                f"order '{external_id}' not found",
                code="ORDER_NOT_FOUND",
            )

        return order

    def list_orders_for_owner(
        self,
        owner_id: int,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> Tuple[List[Order], int]:
        if page < 1:
            raise ValidationError(
                "page must be >= 1",
                code="INVALID_PAGE",
            )

        if limit < 1 or limit > 200:
            raise ValidationError(
                "limit must be between 1 and 200",
                code="INVALID_LIMIT",
            )

        return self.repo.list_for_owner(
            owner_id=owner_id,
            page=page,
            limit=limit,
            status=status,
        )

    def list_all_orders(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Order], int]:
        if page < 1:
            raise ValidationError(
                "page must be >= 1",
                code="INVALID_PAGE",
            )

        if limit < 1 or limit > 200:
            raise ValidationError(
                "limit must be between 1 and 200",
                code="INVALID_LIMIT",
            )

        return self.repo.list_all(
            page=page,
            limit=limit,
            status=status,
            search=search,
        )

    def transition(
        self,
        order_id: int,
        target_status: OrderStatus,
        actor_user_id: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Order:
        order = self.repo.get(order_id)

        if not order:
            raise NotFoundError(
                f"order {order_id} not found",
                code="ORDER_NOT_FOUND",
            )

        current_status = OrderStatus(order.status)

        allowed_targets = self.ALLOWED_TRANSITIONS.get(
            current_status,
            [],
        )

        if target_status not in allowed_targets:
            raise InvalidTransitionError(
                from_status=current_status.value,
                to_status=target_status.value,
                code="INVALID_FSM_TRANSITION",
            )

        if actor_user_id:
            actor = self.user_repo.get(actor_user_id)

            if not actor:
                raise NotFoundError(
                    f"actor {actor_user_id} not found",
                    code="ACTOR_NOT_FOUND",
                )

            if actor.role != "ADMIN":
                raise ForbiddenError(
                    "only admins can transition orders",
                    code="NOT_ADMIN",
                )

        from_status = order.status

        try:
            updated = self.repo.update_status(
                order,
                target_status,
            )

            self.audit.record_order_transition(
                order_id=order.id,
                from_status=str(from_status),
                to_status=target_status.value,
                performed_by=actor_user_id,
                reason=reason,
            )

            self.db.commit()
            self.db.refresh(updated)

            logger.info(
                f"Order {order_id} transitioned "
                f"{from_status} -> {target_status.value}"
            )

            return updated

        except Exception as exc:
            self.db.rollback()

            logger.error(
                f"Transition failed for order "
                f"{order_id}: {exc}"
            )

            raise