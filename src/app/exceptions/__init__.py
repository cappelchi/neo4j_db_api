"""
Expose custom exceptions for use throughout the application.
"""

from .base import (
    BaseAPIException,
    DatabaseError,
    ValidationError,
    AuthenticationError,
    ResourceNotFoundError,
)

__all__ = [
    "BaseAPIException",
    "DatabaseError",
    "ValidationError",
    "AuthenticationError",
    "ResourceNotFoundError",
] 