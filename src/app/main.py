"""
Main FastAPI application module.
This module initializes the FastAPI application with all necessary configurations
and middleware.
"""

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from .exceptions import (
    BaseAPIException,
    DatabaseError,
    ValidationError as CustomValidationError,
    AuthenticationError,
    ResourceNotFoundError,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger: logging.Logger = logging.getLogger(__name__)

# Initialize FastAPI application
app: FastAPI = FastAPI(
    title="Neo4j DB API",
    description="API for interacting with Neo4j database",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next: Any) -> Any:
    """
    Middleware to log incoming requests and their responses.
    
    Args:
        request: The incoming request
        call_next: The next middleware/handler in the chain
        
    Returns:
        The response from the next handler
    """
    logger.info(f"Incoming request: {request.method} {request.url}")
    response: Any = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Global exception handlers
@app.exception_handler(BaseAPIException)
async def base_api_exception_handler(
    request: Request,
    exc: BaseAPIException
) -> JSONResponse:
    """
    Handle all custom API exceptions.
    
    Args:
        request: The incoming request
        exc: The exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error(f"API Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle FastAPI validation errors.
    
    Args:
        request: The incoming request
        exc: The validation error that was raised
        
    Returns:
        JSONResponse with validation error details
    """
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(
    request: Request,
    exc: ValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    
    Args:
        request: The incoming request
        exc: The Pydantic validation error that was raised
        
    Returns:
        JSONResponse with validation error details
    """
    logger.error(f"Pydantic Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handle all other exceptions.
    
    Args:
        request: The incoming request
        exc: The exception that was raised
        
    Returns:
        JSONResponse with generic error message
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health")
async def health_check() -> JSONResponse:
    """
    Basic health check endpoint.
    
    Returns:
        JSONResponse with status information
    """
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200
    )

# API version prefix
API_V1_PREFIX: str = "/api/v1"

# Import and include routers here
# Example: app.include_router(some_router, prefix=API_V1_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    ) 