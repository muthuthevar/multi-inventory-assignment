from datetime import datetime

from pydantic import BaseModel, Field

from app.models.purchase_order import PurchaseOrderStatus
from app.schemas.item import ItemResponse
from app.schemas.vendor import VendorResponse


class PurchaseOrderCreate(BaseModel):
    item_id: int
    vendor_id: int
    quantity: int = Field(gt=0)


class PurchaseOrderStatusUpdate(BaseModel):
    status: PurchaseOrderStatus


class PurchaseOrderResponse(BaseModel):
    id: int
    item_id: int
    vendor_id: int
    quantity: int
    status: PurchaseOrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class PurchaseOrderDetailedResponse(PurchaseOrderResponse):
    item: ItemResponse
    vendor: VendorResponse
