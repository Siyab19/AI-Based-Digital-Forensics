
from getpass import getpass

from neo4j import GraphDatabase


# Neo4j connection configuration
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_DATABASE = "neo4j"


def create_driver(password):
    """Create a Neo4j database driver."""

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, password)
    )

    return driver


def verify_connection(driver):
    """Verify connectivity and execute a test query."""

    driver.verify_connectivity()

    with driver.session(database=NEO4J_DATABASE) as session:

        result = session.run(
            "RETURN 'Forensic Knowledge Graph Connected!' AS status"
        )

        record = result.single()

        return record["status"]


def main():

    print("\nNEO4J KNOWLEDGE GRAPH CONNECTION")
    print("=" * 45)

    password = getpass("Enter your Neo4j password: ")

    driver = None

    try:
        driver = create_driver(password)

        status = verify_connection(driver)

        print("\nConnection successful!")
        print(status)

    except Exception as error:
        print("\nConnection failed.")
        print(f"Error: {error}")

    finally:
        if driver is not None:
            driver.close()
            print("\nDatabase driver closed.")


if __name__ == "__main__":
    main()
