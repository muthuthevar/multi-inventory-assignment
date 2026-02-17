from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vendor import Vendor


class VendorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, vendor: Vendor) -> Vendor:
        self.db.add(vendor)
        self.db.commit()
        self.db.refresh(vendor)
        return vendor

    def get_by_id(self, vendor_id: int) -> Optional[Vendor]:
        return self.db.get(Vendor, vendor_id)

    def get_by_email(self, contact_email: str) -> Optional[Vendor]:
        stmt = select(Vendor).where(Vendor.contact_email == contact_email)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[Vendor]:
        stmt = select(Vendor).order_by(Vendor.id.asc())
        return list(self.db.execute(stmt).scalars().all())
