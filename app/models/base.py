"""SQLAlchemy base configuration and shared mixins."""
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base

# Shared base class for all models to inherit from
Base = declarative_base()


class BaseModel(Base):
    """
    An abstract base class that automatically adds 'created_at'
    and 'updated_at' timestamps to every table in the database.
    """
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # Set on row creation
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
