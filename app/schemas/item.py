from typing import Optional

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    current_stock: int = Field(default=0, ge=0)


class ItemResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    current_stock: int

    model_config = {"from_attributes": True}


class StockAdjustRequest(BaseModel):
    delta: int
