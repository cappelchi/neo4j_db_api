"""
Configuration management for Neo4j database connection settings.

This module handles loading and validating Neo4j connection settings from environment variables.
It uses Pydantic's BaseSettings for automatic environment variable loading and validation.

Required environment variables:
    - NEO4J_URI: The URI of the Neo4j database (e.g., "bolt://localhost:7687")
    - NEO4J_USERNAME: The username for database authentication
    - NEO4J_PASSWORD: The password for database authentication
    - NEO4J_DATABASE: The name of the database to connect to (defaults to "neo4j")
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Neo4jSettings(BaseSettings):
    """
    Neo4j connection settings loaded from environment variables.
    
    This class handles loading and validating Neo4j connection settings from environment variables.
    It uses Pydantic's BaseSettings for automatic environment variable loading and validation.
    
    Attributes:
        NEO4J_URI (str): The URI of the Neo4j database
        NEO4J_USERNAME (str): The username for database authentication
        NEO4J_PASSWORD (str): The password for database authentication
        NEO4J_DATABASE (str): The name of the database to connect to (defaults to "neo4j")
    """
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str = "neo4j"  # Default database name

    def __init__(self, **kwargs):
        """
        Initialize Neo4j settings and log successful loading.
        
        Args:
            **kwargs: Keyword arguments passed to the parent class
        """
        super().__init__(**kwargs)
        logger.info("Neo4j settings loaded from environment variables")


# Create global settings instance
neo4j_settings = Neo4jSettings() 