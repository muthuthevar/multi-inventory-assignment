from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ItemVendor(Base):
    __tablename__ = "item_vendors"
    __table_args__ = (UniqueConstraint("item_id", "vendor_id", name="uq_item_vendor"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
