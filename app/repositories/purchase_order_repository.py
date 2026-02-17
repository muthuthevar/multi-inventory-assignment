from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.purchase_order import PurchaseOrder


class PurchaseOrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, purchase_order: PurchaseOrder) -> PurchaseOrder:
        self.db.add(purchase_order)
        self.db.commit()
        self.db.refresh(purchase_order)
        return purchase_order

    def get_by_id(self, purchase_order_id: int) -> Optional[PurchaseOrder]:
        return self.db.get(PurchaseOrder, purchase_order_id)

    def get_by_id_with_details(self, purchase_order_id: int) -> Optional[PurchaseOrder]:
        stmt = (
            select(PurchaseOrder)
            .options(joinedload(PurchaseOrder.item), joinedload(PurchaseOrder.vendor))
            .where(PurchaseOrder.id == purchase_order_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[PurchaseOrder]:
        stmt = (
            select(PurchaseOrder)
            .options(joinedload(PurchaseOrder.item), joinedload(PurchaseOrder.vendor))
            .order_by(PurchaseOrder.id.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def update(self, purchase_order: PurchaseOrder) -> PurchaseOrder:
        self.db.add(purchase_order)
        self.db.commit()
        self.db.refresh(purchase_order)
        return purchase_order
