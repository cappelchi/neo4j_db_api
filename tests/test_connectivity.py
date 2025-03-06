"""
Tests for database connectivity verification endpoint.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from neo4j.exceptions import ServiceUnavailable, SessionExpired

from app.main import app
from app.models.connectivity import ConnectivityResponse

# Create test client
client = TestClient(app)

# Test data
SUCCESS_RESPONSE = {
    "status": True,
    "message": "Successfully connected to Neo4j database"
}

FAILURE_RESPONSE = {
    "status": False,
    "message": "Database service is unavailable"
}


@pytest.fixture
def mock_neo4j_driver():
    """Fixture to mock Neo4j driver."""
    with patch("app.db.connectivity.GraphDatabase") as mock_graph_db:
        yield mock_graph_db


def test_successful_connection(mock_neo4j_driver):
    """Test successful database connection verification."""
    # Mock successful connection
    mock_driver = Mock()
    mock_driver.verify_connectivity.return_value = None
    mock_neo4j_driver.driver.return_value = mock_driver
    
    # Make request to endpoint
    response = client.get("/api/v1/verify-connectivity")
    
    # Assert response
    assert response.status_code == 200
    assert response.json() == SUCCESS_RESPONSE


def test_service_unavailable(mock_neo4j_driver):
    """Test database service unavailable error."""
    # Mock service unavailable error
    mock_driver = Mock()
    mock_driver.verify_connectivity.side_effect = ServiceUnavailable("Service unavailable")
    mock_neo4j_driver.driver.return_value = mock_driver
    
    # Make request to endpoint
    response = client.get("/api/v1/verify-connectivity")
    
    # Assert response
    assert response.status_code == 503
    assert response.json()["detail"] == "Database service is unavailable"


def test_session_expired(mock_neo4j_driver):
    """Test session expired error."""
    # Mock session expired error
    mock_driver = Mock()
    mock_driver.verify_connectivity.side_effect = SessionExpired("Session expired")
    mock_neo4j_driver.driver.return_value = mock_driver
    
    # Make request to endpoint
    response = client.get("/api/v1/verify-connectivity")
    
    # Assert response
    assert response.status_code == 503
    assert response.json()["detail"] == "Database session expired"


def test_unexpected_error(mock_neo4j_driver):
    """Test unexpected error handling."""
    # Mock unexpected error
    mock_driver = Mock()
    mock_driver.verify_connectivity.side_effect = Exception("Unexpected error")
    mock_neo4j_driver.driver.return_value = mock_driver
    
    # Make request to endpoint
    response = client.get("/api/v1/verify-connectivity")
    
    # Assert response
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error while verifying database connectivity"


def test_response_model_validation():
    """Test response model validation."""
    # Test valid response
    valid_response = ConnectivityResponse(
        status=True,
        message="Successfully connected to Neo4j database"
    )
    assert valid_response.status is True
    assert valid_response.message == "Successfully connected to Neo4j database"
    
    # Test invalid response (should raise validation error)
    with pytest.raises(ValueError):
        ConnectivityResponse(
            status="invalid",  # Should be bool
            message=123  # Should be str
        ) 