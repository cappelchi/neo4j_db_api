"""
Router for database connectivity verification endpoints.

This module provides the FastAPI router for database connectivity verification.
It exposes a GET endpoint that checks if the application can connect to the
Neo4j database.

Endpoints:
    GET /verify-connectivity
        Verifies connectivity to the Neo4j database.
        
        Returns:
            200: Successfully connected to database
            503: Database service unavailable
            500: Internal server error
            
        Example Response:
            {
                "status": true,
                "message": "Successfully connected to Neo4j database"
            }
"""

import logging
from fastapi import APIRouter, HTTPException

from app.db.connectivity import verify_connection
from app.models.connectivity import ConnectivityResponse

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/verify-connectivity",
    tags=["connectivity"],
    responses={
        200: {"description": "Successfully verified database connectivity"},
        503: {"description": "Database service unavailable"},
        500: {"description": "Internal server error"}
    }
)


@router.get(
    "",
    response_model=ConnectivityResponse,
    summary="Verify database connectivity",
    description="Checks if the application can connect to the Neo4j database."
)
async def check_connectivity() -> ConnectivityResponse:
    """
    Verify connectivity to the Neo4j database.
    
    This endpoint attempts to establish a connection to the Neo4j database
    and returns the connection status. It handles various error scenarios
    and provides appropriate HTTP status codes and error messages.
    
    Returns:
        ConnectivityResponse: Response containing connection status and message
        
    Raises:
        HTTPException: 
            - 503: If the database service is unavailable
            - 500: If there's an unexpected error
            
    Example Response:
        {
            "status": true,
            "message": "Successfully connected to Neo4j database"
        }
    """
    logger.info("Received request to verify database connectivity")
    
    try:
        status, message = verify_connection()
        
        if not status:
            logger.error(f"Database connectivity check failed: {message}")
            raise HTTPException(
                status_code=503,
                detail=message
            )
            
        logger.info("Database connectivity check successful")
        return ConnectivityResponse(
            status=status,
            message=message
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error during connectivity check: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while verifying database connectivity"
        ) 