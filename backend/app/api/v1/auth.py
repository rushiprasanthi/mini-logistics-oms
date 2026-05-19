from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success, error
from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.services.auth_service import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    summary="Register a new user",
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    existing = repo.get_by_email(
        payload.email
    )

    if existing:
        return error(
            message="email_already_registered",
            code=409,
            error_code="EMAIL_EXISTS",
        )

    # IMPORTANT FIX
    # New users become ADMIN automatically
    user = repo.create(
        email=payload.email,
        hashed_password=hash_password(
            payload.password
        ),
        role="ADMIN",
    )

    db.commit()

    return success(
        {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        },
        message="user_registered",
    )


@router.post(
    "/login",
    summary="Authenticate user and return JWT",
)
def login(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    user = repo.get_by_email(
        payload.email
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.hashed_password,
        )
    ):
        return error(
            message="invalid_credentials",
            code=401,
            error_code="INVALID_CREDENTIALS",
        )

    token = create_access_token(
        subject=str(user.id)
    )

    return success(
        {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            },
        },
        message="login_successful",
    )