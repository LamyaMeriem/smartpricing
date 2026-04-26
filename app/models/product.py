"""Product and ProductVariant models."""

import enum
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ProductSource(str, enum.Enum):
    """
    Defines the origin of the product data.
    Useful for tracking imports from different e-commerce platforms or manual entry.
    """
    MANUAL = "manual"
    PRESTASHOP = "prestashop"
    CSV = "csv"


class Product(BaseModel):
    """
    Represents a high-level product category or model (e.g., 'iPhone 12').
    This acts as a container for various versions (variants) of the same item.
    """
    __tablename__ = "products"

    # Primary key using UUID for global uniqueness and security
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # General descriptive information shared by all variants
    name = Column(String(255), nullable=False)
    model = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # Tracking where this product data came from
    source = Column(Enum(ProductSource), nullable=False, default=ProductSource.MANUAL)
    source_id = Column(String(100), nullable=True, index=True)

    # One-to-Many relationship: A product can have multiple variants (e.g., different colors/storage).
    # 'cascade' ensures that if a Product is deleted, its variants are also deleted from the DB.
    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        """String representation for debugging and logging."""
        return f"<Product(id={self.id}, name={self.name})>"


class ProductVariant(BaseModel):
    """
    Represents a specific Stock Keeping Unit (SKU).
    This is the actual sellable item with specific attributes like color, size, or condition.
    """
    __tablename__ = "product_variants"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key link back to the parent Product
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)

    # Unique SKU for inventory management and identification
    sku = Column(String(80), unique=True, nullable=False, index=True)

    # Specific attributes that differentiate this variant
    storage = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    grade = Column(String(50), nullable=True)

    # Pricing and Inventory data
    # Numeric(10, 2) allows up to 10 digits total with 2 decimal places.
    current_price = Column(Numeric(10, 2), nullable=True)
    current_stock = Column(Integer, nullable=False, default=0)

    # Source tracking for the specific variant
    source = Column(Enum(ProductSource), nullable=False, default=ProductSource.MANUAL)
    source_id = Column(String(100), nullable=True, index=True)

    # Many-to-One relationship back to the parent Product
    product = relationship("Product", back_populates="variants")

    def __repr__(self):
        """String representation for debugging and logging."""
        return f"<ProductVariant(sku={self.sku}, stock={self.current_stock})>"
