from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.core.rbac import get_current_active_user
from app.core.responses import success
from app.db.session import get_db
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate
from app.services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post(
    "/",
    summary="Create order",
)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = OrderService(db)

    try:
        order = service.create_order(
            external_id=payload.external_id,
            customer_id=current_user.id,
        )

        db.flush()
        db.commit()
        db.refresh(order)

        return success(
            order,
            message="order_created",
        )

    except Exception:
        db.rollback()
        raise


@router.get(
    "/my",
    summary="List my orders",
)
def list_my_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = OrderService(db)

    items, total = service.list_orders_for_owner(
        owner_id=current_user.id,
        page=page,
        limit=limit,
        status=status,
    )

    return success(
        items,
        meta={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (
                (total + limit - 1) // limit
            ),
        },
    )


@router.patch(
    "/{order_id}/status/{target_status}",
    summary="Transition order status",
)
def transition_order(
    order_id: int = Path(...),
    target_status: OrderStatus = Path(...),
    reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = OrderService(db)

    updated = service.transition(
        order_id=order_id,
        target_status=target_status,
        actor_user_id=current_user.id,
        reason=reason,
    )

    db.commit()

    return success(
        updated,
        message="order_transitioned",
    )
