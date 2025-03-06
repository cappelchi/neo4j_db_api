"""
Shared test fixtures and configuration.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def test_client():
    """Fixture to create a test client."""
    return TestClient(app) 