from fastapi import APIRouter

from app.api.routes.items import router as items_router
from app.api.routes.purchase_orders import router as purchase_orders_router
from app.api.routes.vendors import router as vendors_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(items_router)
api_router.include_router(vendors_router)
api_router.include_router(purchase_orders_router)
