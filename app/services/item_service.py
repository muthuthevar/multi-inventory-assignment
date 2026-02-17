from typing import Protocol
from typing import Optional

from fastapi import HTTPException, status

from app.models.item import Item
from app.schemas.item import ItemCreate


class ItemRepositoryPort(Protocol):
    def create(self, item: Item) -> Item: ...
    def get_by_id(self, item_id: int) -> Optional[Item]: ...
    def get_by_sku(self, sku: str) -> Optional[Item]: ...
    def list_all(self) -> list[Item]: ...
    def update(self, item: Item) -> Item: ...
    def create_vendor_link(self, item_id: int, vendor_id: int, is_approved: bool = True): ...
    def get_vendor_link(self, item_id: int, vendor_id: int): ...
    def list_approved_vendors(self, item_id: int): ...


class VendorRepositoryPort(Protocol):
    def get_by_id(self, vendor_id: int): ...


class ItemService:
    def __init__(self, item_repo: ItemRepositoryPort, vendor_repo: VendorRepositoryPort) -> None:
        self.item_repo = item_repo
        self.vendor_repo = vendor_repo

    def create_item(self, payload: ItemCreate) -> Item:
        if self.item_repo.get_by_sku(payload.sku):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with SKU '{payload.sku}' already exists.",
            )

        item = Item(
            sku=payload.sku,
            name=payload.name,
            description=payload.description,
            current_stock=payload.current_stock,
        )
        return self.item_repo.create(item)

    def list_items(self) -> list[Item]:
        return self.item_repo.list_all()

    def get_item_or_404(self, item_id: int) -> Item:
        item = self.item_repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
        return item

    def adjust_stock(self, item_id: int, delta: int) -> Item:
        item = self.get_item_or_404(item_id)
        next_stock = item.current_stock + delta
        if next_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock adjustment would result in negative inventory.",
            )
        item.current_stock = next_stock
        return self.item_repo.update(item)

    def link_vendor(self, item_id: int, vendor_id: int, is_approved: bool = True):
        self.get_item_or_404(item_id)
        vendor = self.vendor_repo.get_by_id(vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found.")
        if self.item_repo.get_vendor_link(item_id=item_id, vendor_id=vendor_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vendor is already linked to this item.",
            )
        return self.item_repo.create_vendor_link(item_id=item_id, vendor_id=vendor_id, is_approved=is_approved)

    def list_approved_vendors(self, item_id: int):
        self.get_item_or_404(item_id)
        return self.item_repo.list_approved_vendors(item_id=item_id)
