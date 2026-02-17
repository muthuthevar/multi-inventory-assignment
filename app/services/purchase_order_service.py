from typing import Protocol
from typing import Optional

from fastapi import HTTPException, status

from app.models.purchase_order import PurchaseOrder, PurchaseOrderStatus
from app.schemas.purchase_order import PurchaseOrderCreate


class PurchaseOrderRepositoryPort(Protocol):
    def create(self, purchase_order: PurchaseOrder) -> PurchaseOrder: ...
    def get_by_id(self, purchase_order_id: int) -> Optional[PurchaseOrder]: ...
    def get_by_id_with_details(self, purchase_order_id: int) -> Optional[PurchaseOrder]: ...
    def list_all(self) -> list[PurchaseOrder]: ...
    def update(self, purchase_order: PurchaseOrder) -> PurchaseOrder: ...


class ItemRepositoryPort(Protocol):
    def get_by_id(self, item_id: int): ...
    def get_vendor_link(self, item_id: int, vendor_id: int): ...
    def update(self, item): ...


class VendorRepositoryPort(Protocol):
    def get_by_id(self, vendor_id: int): ...


class PurchaseOrderService:
    def __init__(
        self,
        po_repo: PurchaseOrderRepositoryPort,
        item_repo: ItemRepositoryPort,
        vendor_repo: VendorRepositoryPort,
    ) -> None:
        self.po_repo = po_repo
        self.item_repo = item_repo
        self.vendor_repo = vendor_repo

    def create_purchase_order(self, payload: PurchaseOrderCreate) -> PurchaseOrder:
        item = self.item_repo.get_by_id(payload.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

        vendor = self.vendor_repo.get_by_id(payload.vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found.")
        if not vendor.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vendor is not active.")

        link = self.item_repo.get_vendor_link(item_id=payload.item_id, vendor_id=payload.vendor_id)
        if not link or not link.is_approved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected vendor is not approved for this item.",
            )

        purchase_order = PurchaseOrder(
            item_id=payload.item_id,
            vendor_id=payload.vendor_id,
            quantity=payload.quantity,
        )
        return self.po_repo.create(purchase_order)

    def list_purchase_orders(self) -> list[PurchaseOrder]:
        return self.po_repo.list_all()

    def get_purchase_order_or_404(self, purchase_order_id: int) -> PurchaseOrder:
        purchase_order = self.po_repo.get_by_id_with_details(purchase_order_id)
        if not purchase_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found.")
        return purchase_order

    def update_status(self, purchase_order_id: int, next_status: PurchaseOrderStatus) -> PurchaseOrder:
        purchase_order = self.po_repo.get_by_id(purchase_order_id)
        if not purchase_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found.")

        current_status = purchase_order.status
        if current_status == PurchaseOrderStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled purchase orders cannot be changed.",
            )
        if current_status == next_status:
            return purchase_order
        if current_status == PurchaseOrderStatus.RECEIVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Received purchase orders are final.",
            )

        purchase_order.status = next_status
        purchase_order = self.po_repo.update(purchase_order)

        # Stock is updated only when an order is marked as received.
        if next_status == PurchaseOrderStatus.RECEIVED:
            item = self.item_repo.get_by_id(purchase_order.item_id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Linked item was not found while updating stock.",
                )
            item.current_stock += purchase_order.quantity
            self.item_repo.update(item)

        return purchase_order
