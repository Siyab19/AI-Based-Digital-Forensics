
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from src.config import PROJECT_ROOT


# Load environment variables from the project root.
load_dotenv(PROJECT_ROOT / ".env")


# Read Neo4j configuration.
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


# Validate required configuration.
if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
    raise RuntimeError(
        "Neo4j configuration is incomplete. "
        "Check your project-root .env file."
    )


# Shared database driver.
_driver = None


def connect_to_neo4j():
    """Create and verify the Neo4j database connection."""
    global _driver

    if _driver is None:
        _driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

    _driver.verify_connectivity()

    print("Connected to Neo4j successfully!")


def close_neo4j_connection():
    """Close the shared Neo4j driver."""
    global _driver

    if _driver is not None:
        _driver.close()
        _driver = None

    print("Neo4j connection closed.")


def get_session():
    """Provide a Neo4j session for API requests."""
    if _driver is None:
        raise RuntimeError("Neo4j database is not connected.")

    with _driver.session(database=NEO4J_DATABASE) as session:
        yield session
