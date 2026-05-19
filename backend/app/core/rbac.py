from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ForbiddenError,
    UnauthorizedError,
)
from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.utils.jwt import get_current_user


def get_current_active_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    if not user_id:
        raise UnauthorizedError(
            "missing_token",
            code="MISSING_TOKEN",
        )

    user = UserRepository(db).get(user_id)

    if not user:
        raise UnauthorizedError(
            "user_not_found",
            code="USER_NOT_FOUND",
        )

    if not getattr(user, "is_active", True):
        raise ForbiddenError(
            "inactive_user",
            code="INACTIVE_USER",
        )

    return user


def require_role(required_role: str):
    def role_checker(
        current_user=Depends(
            get_current_active_user
        ),
    ):
        if current_user.role != required_role:
            raise ForbiddenError(
                "insufficient_permissions",
                code="INSUFFICIENT_ROLE",
            )

        return current_user

    return role_checker
