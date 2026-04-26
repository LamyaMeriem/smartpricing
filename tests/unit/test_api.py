"""Unit tests for public and placeholder API endpoints."""
import pytest


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_check(client):
    """Test readiness check endpoint"""
    response = client.get("/readiness")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SmartPricing Engine"
    assert "version" in data


def test_list_products(client):
    """Test list products endpoint"""
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert "products" in response.json()


def test_get_product(client):
    """Test get product endpoint"""
    response = client.get("/api/v1/products/123")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "123"
