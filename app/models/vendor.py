from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    item_links = relationship("ItemVendor", backref="vendor", cascade="all, delete-orphan")
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
