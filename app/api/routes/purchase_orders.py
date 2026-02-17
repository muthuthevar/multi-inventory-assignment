from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_purchase_order_service
from app.schemas.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderDetailedResponse,
    PurchaseOrderResponse,
    PurchaseOrderStatusUpdate,
)
from app.services.purchase_order_service import PurchaseOrderService


router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])


@router.post("", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    payload: PurchaseOrderCreate,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
) -> PurchaseOrderResponse:
    return service.create_purchase_order(payload)


@router.get("", response_model=list[PurchaseOrderDetailedResponse])
def list_purchase_orders(
    service: PurchaseOrderService = Depends(get_purchase_order_service),
) -> list[PurchaseOrderDetailedResponse]:
    return service.list_purchase_orders()


@router.get("/{purchase_order_id}", response_model=PurchaseOrderDetailedResponse)
def get_purchase_order(
    purchase_order_id: int,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
) -> PurchaseOrderDetailedResponse:
    return service.get_purchase_order_or_404(purchase_order_id)


@router.patch("/{purchase_order_id}/status", response_model=PurchaseOrderResponse)
def update_purchase_order_status(
    purchase_order_id: int,
    payload: PurchaseOrderStatusUpdate,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
) -> PurchaseOrderResponse:
    return service.update_status(purchase_order_id=purchase_order_id, next_status=payload.status)
