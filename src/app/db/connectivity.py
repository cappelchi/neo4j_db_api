"""
Neo4j database connectivity verification module.

This module provides functionality to verify connectivity to the Neo4j database.
It handles various connection scenarios and provides appropriate error messages.

Error Handling:
    - ServiceUnavailable: When the database service is not accessible
    - SessionExpired: When the database session has expired
    - General exceptions: For unexpected errors during connection verification

Example:
    >>> status, message = verify_connection()
    >>> if status:
    ...     print("Successfully connected to database")
    ... else:
    ...     print(f"Connection failed: {message}")
"""

import logging
from typing import Tuple

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, SessionExpired

from app.core.config import neo4j_settings

# Configure logging
logger = logging.getLogger(__name__)


def verify_connection() -> Tuple[bool, str]:
    """
    Verify connectivity to the Neo4j database.
    
    This function attempts to establish a connection to the Neo4j database using
    the configured settings. It handles various error scenarios and provides
    appropriate status messages.
    
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if connection is successful, False otherwise
            - str: Status message describing the result
            
    Example:
        >>> status, message = verify_connection()
        >>> if status:
        ...     print("Successfully connected to database")
        ... else:
        ...     print(f"Connection failed: {message}")
    """
    logger.info("Attempting to verify Neo4j database connectivity")
    
    try:
        # Create a driver instance
        driver: Driver = GraphDatabase.driver(
            neo4j_settings.NEO4J_URI,
            auth=(neo4j_settings.NEO4J_USERNAME, neo4j_settings.NEO4J_PASSWORD)
        )
        
        # Try to connect and verify the connection
        driver.verify_connectivity()
        
        # If we get here, connection was successful
        logger.info("Successfully verified Neo4j database connectivity")
        return True, "Successfully connected to Neo4j database"
        
    except ServiceUnavailable as e:
        logger.error(f"Failed to connect to Neo4j database: {str(e)}")
        return False, "Database service is unavailable"
        
    except SessionExpired as e:
        logger.error(f"Neo4j session expired: {str(e)}")
        return False, "Database session expired"
        
    except Exception as e:
        logger.error(f"Unexpected error while verifying Neo4j connectivity: {str(e)}")
        return False, f"Connection failed: {str(e)}"
        
    finally:
        # Always close the driver
        try:
            driver.close()
        except Exception as e:
            logger.warning(f"Error while closing Neo4j driver: {str(e)}") 