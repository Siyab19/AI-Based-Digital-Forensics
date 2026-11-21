from src.api.database import (
    connect_to_neo4j,
    close_neo4j_connection
)

try:
    connect_to_neo4j()
    print("FastAPI database configuration is working!")

except Exception as error:
    print(f"Connection failed: {error}")

finally:
    close_neo4j_connection()