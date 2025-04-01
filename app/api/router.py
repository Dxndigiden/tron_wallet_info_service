from fastapi import APIRouter
from app.api.endpoints.wallet import router as wallet_router

router = APIRouter()

router.include_router(
    wallet_router,
    prefix='/api',
    tags=['ручки Tron Wallet']
)
