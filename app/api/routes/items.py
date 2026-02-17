from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_item_service
from app.schemas.item import ItemCreate, ItemResponse, StockAdjustRequest
from app.schemas.vendor import VendorResponse
from app.services.item_service import ItemService


router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)) -> ItemResponse:
    return service.create_item(payload)


@router.get("", response_model=list[ItemResponse])
def list_items(service: ItemService = Depends(get_item_service)) -> list[ItemResponse]:
    return service.list_items()


@router.patch("/{item_id}/stock", response_model=ItemResponse)
def adjust_stock(
    item_id: int,
    payload: StockAdjustRequest,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    return service.adjust_stock(item_id=item_id, delta=payload.delta)


@router.post("/{item_id}/vendors/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_vendor_to_item(item_id: int, vendor_id: int, service: ItemService = Depends(get_item_service)) -> None:
    service.link_vendor(item_id=item_id, vendor_id=vendor_id, is_approved=True)
    return None


@router.get("/{item_id}/approved-vendors", response_model=list[VendorResponse])
def list_approved_vendors(item_id: int, service: ItemService = Depends(get_item_service)) -> list[VendorResponse]:
    return service.list_approved_vendors(item_id=item_id)
