from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_vendor_service
from app.schemas.vendor import VendorCreate, VendorResponse
from app.services.vendor_service import VendorService


router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(payload: VendorCreate, service: VendorService = Depends(get_vendor_service)) -> VendorResponse:
    return service.create_vendor(payload)


@router.get("", response_model=list[VendorResponse])
def list_vendors(service: VendorService = Depends(get_vendor_service)) -> list[VendorResponse]:
    return service.list_vendors()
