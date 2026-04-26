"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Test client for FastAPI"""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Mock auth headers"""
    return {"Authorization": "Bearer fake-token"}
