from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.item_repository import ItemRepository
from app.repositories.purchase_order_repository import PurchaseOrderRepository
from app.repositories.vendor_repository import VendorRepository
from app.services.item_service import ItemService
from app.services.purchase_order_service import PurchaseOrderService
from app.services.vendor_service import VendorService


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(item_repo=ItemRepository(db), vendor_repo=VendorRepository(db))


def get_vendor_service(db: Session = Depends(get_db)) -> VendorService:
    return VendorService(vendor_repo=VendorRepository(db))


def get_purchase_order_service(db: Session = Depends(get_db)) -> PurchaseOrderService:
    return PurchaseOrderService(
        po_repo=PurchaseOrderRepository(db),
        item_repo=ItemRepository(db),
        vendor_repo=VendorRepository(db),
    )
