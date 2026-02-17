from typing import Protocol
from typing import Optional

from fastapi import HTTPException, status

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate


class VendorRepositoryPort(Protocol):
    def create(self, vendor: Vendor) -> Vendor: ...
    def get_by_id(self, vendor_id: int) -> Optional[Vendor]: ...
    def get_by_email(self, contact_email: str) -> Optional[Vendor]: ...
    def list_all(self) -> list[Vendor]: ...


class VendorService:
    def __init__(self, vendor_repo: VendorRepositoryPort) -> None:
        self.vendor_repo = vendor_repo

    def create_vendor(self, payload: VendorCreate) -> Vendor:
        if self.vendor_repo.get_by_email(payload.contact_email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vendor email '{payload.contact_email}' already exists.",
            )

        vendor = Vendor(
            name=payload.name,
            contact_email=payload.contact_email,
            is_active=payload.is_active,
        )
        return self.vendor_repo.create(vendor)

    def list_vendors(self) -> list[Vendor]:
        return self.vendor_repo.list_all()

    def get_vendor_or_404(self, vendor_id: int) -> Vendor:
        vendor = self.vendor_repo.get_by_id(vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found.")
        return vendor
