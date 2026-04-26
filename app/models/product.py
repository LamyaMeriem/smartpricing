"""Product and ProductVariant models."""

import enum
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ProductSource(str, enum.Enum):
    MANUAL = "manual"
    PRESTASHOP = "prestashop"
    CSV = "csv"


class Product(BaseModel):
    """Parent product (ex: iPhone 12)"""

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)
    model = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    source = Column(Enum(ProductSource), nullable=False, default=ProductSource.MANUAL)
    source_id = Column(String(100), nullable=True, index=True)

    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"


class ProductVariant(BaseModel):
    """Sellable unit (ex: iPhone 12 / 128GB / Black / Grade A)"""

    __tablename__ = "product_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)

    sku = Column(String(80), unique=True, nullable=False, index=True)

    storage = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    grade = Column(String(50), nullable=True)

    current_price = Column(Numeric(10, 2), nullable=True)
    current_stock = Column(Integer, nullable=False, default=0)

    source = Column(Enum(ProductSource), nullable=False, default=ProductSource.MANUAL)
    source_id = Column(String(100), nullable=True, index=True)

    product = relationship("Product", back_populates="variants")

    def __repr__(self):
        return f"<ProductVariant(sku={self.sku}, stock={self.current_stock})>"