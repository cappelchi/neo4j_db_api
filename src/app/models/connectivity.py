"""
Response models for database connectivity verification.

This module defines the Pydantic models used for the database connectivity
verification endpoint responses. It includes validation and example data
for API documentation.

Example Response:
    {
        "status": true,
        "message": "Successfully connected to Neo4j database"
    }
"""

from pydantic import BaseModel, Field


class ConnectivityResponse(BaseModel):
    """
    Response model for database connectivity verification.
    
    This model defines the structure of the response returned by the
    database connectivity verification endpoint.
    
    Attributes:
        status (bool): True if connection is successful, False otherwise
        message (str): Status message describing the result
        
    Example:
        >>> response = ConnectivityResponse(
        ...     status=True,
        ...     message="Successfully connected to Neo4j database"
        ... )
        >>> print(response.json())
        {
            "status": true,
            "message": "Successfully connected to Neo4j database"
        }
    """
    status: bool = Field(
        description="True if connection is successful, False otherwise"
    )
    message: str = Field(
        description="Status message describing the result"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully connected to Neo4j database"
            }
        } 