"""
Tests for main application endpoints and functionality.
"""

import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client: TestClient = TestClient(app)


def test_health_check() -> None:
    """
    Test the health check endpoint.
    
    Verifies that:
    1. The endpoint returns 200 status code
    2. The response contains the expected status message
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_api_docs_available() -> None:
    """
    Test that API documentation endpoints are available.
    
    Verifies that:
    1. Swagger UI is accessible
    2. ReDoc is accessible
    3. OpenAPI schema is accessible
    """
    # Test Swagger UI
    response = client.get("/api/docs")
    assert response.status_code == 200
    
    # Test ReDoc
    response = client.get("/api/redoc")
    assert response.status_code == 200
    
    # Test OpenAPI schema
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json() 