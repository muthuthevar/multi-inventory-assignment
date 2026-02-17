from pydantic import BaseModel, EmailStr, Field


class VendorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    contact_email: EmailStr
    is_active: bool = True


class VendorResponse(BaseModel):
    id: int
    name: str
    contact_email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}
