from fastapi import APIRouter

from app.api.v1 import auth, orders

router = APIRouter()

# Auth and Orders routers already have their prefixes
router.include_router(auth.router)
router.include_router(orders.router)
