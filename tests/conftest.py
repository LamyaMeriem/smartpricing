"""Pytest configuration and fixtures."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies import get_db
from app.main import app


class FakeQuery:
    """Fake SQLAlchemy query object for unit tests."""

    def all(self) -> list:
        """Return an empty list."""
        return []


class FakeSession:
    """Fake database session for unit tests."""

    def query(self, model):
        """Return a fake query object."""
        return FakeQuery()

    def close(self) -> None:
        """Close fake session."""


def override_get_db() -> Generator[FakeSession, None, None]:
    """Override database dependency for unit tests."""
    db = FakeSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Test client for FastAPI."""
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    """Mock auth headers."""
    return {"Authorization": "Bearer fake-token"}
