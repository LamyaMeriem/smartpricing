"""Database base imports."""

# Base class
from app.models.base import Base  # noqa: F401

# Import models to register them with SQLAlchemy metadata
import app.models.product  # noqa: F401
import app.models.user  # noqa: F401
