"""
Neo4j database utilities and connection management.
"""

import logging
from typing import Any, Dict, Optional, Generator

from fastapi import Depends
from neo4j import GraphDatabase, Driver, Session, Transaction

from app.core.config import neo4j_settings

# Configure logging
logger: logging.Logger = logging.getLogger(__name__)


def get_neo4j_driver() -> Generator[Driver, None, None]:
    """
    Create and yield a Neo4j driver instance.
    
    Yields:
        Driver: Neo4j driver instance
        
    Note:
        The driver is automatically closed when the generator is exhausted.
    """
    logger.debug(f"Creating Neo4j driver with URI: {neo4j_settings.NEO4J_URI}")
    driver: Driver = GraphDatabase.driver(
        neo4j_settings.NEO4J_URI,
        auth=(neo4j_settings.NEO4J_USERNAME, neo4j_settings.NEO4J_PASSWORD)
    )
    try:
        yield driver
    finally:
        driver.close()


# Type alias for dependency injection
Neo4jDriverDependency = Depends(get_neo4j_driver)


def get_neo4j_session(driver: Driver = Neo4jDriverDependency) -> Generator[Session, None, None]:
    """
    Create and yield a Neo4j session instance.
    
    Args:
        driver: Neo4j driver instance
        
    Yields:
        Session: Neo4j session instance
        
    Note:
        The session is automatically closed when the generator is exhausted.
    """
    session: Session = driver.session(database=neo4j_settings.NEO4J_DATABASE)
    try:
        yield session
    finally:
        session.close()


def execute_query(
    tx: Transaction,
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Execute a parameterized Cypher query within a transaction.
    
    Args:
        tx: Neo4j transaction instance
        query: Cypher query string
        params: Query parameters
        
    Returns:
        Query result
        
    Note:
        Always use parameterized queries to prevent Cypher injection.
    """
    if params is None:
        params = {}
    
    logger.debug(f"Executing query: {query} with params: {params}")
    result = tx.run(query, params)
    return result 