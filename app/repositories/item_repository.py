from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.item import Item
from app.models.item_vendor import ItemVendor
from app.models.vendor import Vendor


class ItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self.db.get(Item, item_id)

    def get_by_sku(self, sku: str) -> Optional[Item]:
        stmt = select(Item).where(Item.sku == sku)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[Item]:
        stmt = select(Item).order_by(Item.id.asc())
        return list(self.db.execute(stmt).scalars().all())

    def update(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def create_vendor_link(self, item_id: int, vendor_id: int, is_approved: bool = True) -> ItemVendor:
        link = ItemVendor(item_id=item_id, vendor_id=vendor_id, is_approved=is_approved)
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link

    def get_vendor_link(self, item_id: int, vendor_id: int) -> Optional[ItemVendor]:
        stmt = select(ItemVendor).where(ItemVendor.item_id == item_id, ItemVendor.vendor_id == vendor_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_approved_vendors(self, item_id: int) -> list[Vendor]:
        stmt = (
            select(Vendor)
            .join(ItemVendor, ItemVendor.vendor_id == Vendor.id)
            .where(ItemVendor.item_id == item_id, ItemVendor.is_approved.is_(True))
            .order_by(Vendor.id.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_with_details(self, item_id: int) -> Optional[Item]:
        stmt = (
            select(Item)
            .options(joinedload(Item.vendor_links))
            .where(Item.id == item_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()
