
import hashlib
import json
from getpass import getpass

from neo4j import GraphDatabase

from src.config import (
    NORMALIZED_EVIDENCE_FILE,
    SEQUENCES_FILE,
    CORRELATIONS_FILE,
    GENERATED_DATA_DIR
)

from src.knowledge_graph.graph_connection import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_DATABASE
)


# --------------------------------------------------
# File paths
# --------------------------------------------------

HYBRID_ANALYSIS_FILE = GENERATED_DATA_DIR / "hybrid_analysis.json"


# --------------------------------------------------
# Event identity
# --------------------------------------------------

IDENTITY_FIELDS = [
    "timestamp",
    "source",
    "event_type",
    "user",
    "source_ip",
    "destination_ip",
    "device",
    "action",
    "status",
    "resource"
]


def generate_event_id(event):

    identity = {
        field: event.get(field)
        for field in IDENTITY_FIELDS
    }

    serialized = json.dumps(
        identity,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


# --------------------------------------------------
# Load JSON files
# --------------------------------------------------

def load_json(filename):

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Create database constraints
# --------------------------------------------------

def create_constraints(session):

    constraints = [
        """
        CREATE CONSTRAINT user_name_unique IF NOT EXISTS
        FOR (u:User)
        REQUIRE u.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT ip_address_unique IF NOT EXISTS
        FOR (ip:IPAddress)
        REQUIRE ip.address IS UNIQUE
        """,
        """
        CREATE CONSTRAINT device_name_unique IF NOT EXISTS
        FOR (d:Device)
        REQUIRE d.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT event_id_unique IF NOT EXISTS
        FOR (e:EvidenceEvent)
        REQUIRE e.event_id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT sequence_id_unique IF NOT EXISTS
        FOR (s:Sequence)
        REQUIRE s.sequence_id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT finding_sequence_unique IF NOT EXISTS
        FOR (f:InvestigationFinding)
        REQUIRE f.sequence_id IS UNIQUE
        """
    ]

    for constraint in constraints:
        session.run(constraint).consume()


# --------------------------------------------------
# Create or update evidence events and entities
# --------------------------------------------------

def merge_event(tx, event):

    event_id = generate_event_id(event)

    properties = {
        "event_id": event_id,
        "timestamp": event.get("timestamp"),
        "source": event.get("source"),
        "event_type": event.get("event_type"),
        "action": event.get("action"),
        "status": event.get("status"),
        "resource": event.get("resource"),
        "details_json": json.dumps(
            event.get("details") or {},
            sort_keys=True
        )
    }

    tx.run(
        """
        MERGE (e:EvidenceEvent {event_id: $event_id})
        SET e += $properties
        """,
        event_id=event_id,
        properties=properties
    ).consume()

    if event.get("user"):

        tx.run(
            """
            MERGE (u:User {name: $name})
            WITH u
            MATCH (e:EvidenceEvent {event_id: $event_id})
            MERGE (e)-[:INVOLVES_USER]->(u)
            """,
            name=event["user"].lower(),
            event_id=event_id
        ).consume()

    if event.get("source_ip"):

        tx.run(
            """
            MERGE (ip:IPAddress {address: $address})
            WITH ip
            MATCH (e:EvidenceEvent {event_id: $event_id})
            MERGE (e)-[:ORIGINATED_FROM]->(ip)
            """,
            address=event["source_ip"],
            event_id=event_id
        ).consume()

    if event.get("destination_ip"):

        tx.run(
            """
            MERGE (ip:IPAddress {address: $address})
            WITH ip
            MATCH (e:EvidenceEvent {event_id: $event_id})
            MERGE (e)-[:CONNECTED_TO]->(ip)
            """,
            address=event["destination_ip"],
            event_id=event_id
        ).consume()

    if event.get("device"):

        tx.run(
            """
            MERGE (d:Device {name: $name})
            WITH d
            MATCH (e:EvidenceEvent {event_id: $event_id})
            MERGE (e)-[:OBSERVED_ON]->(d)
            """,
            name=event["device"],
            event_id=event_id
        ).consume()

    return event_id


# --------------------------------------------------
# Create sequences and chronological relationships
# --------------------------------------------------

def merge_sequence(tx, sequence):

    sequence_id = sequence["sequence_id"]

    tx.run(
        """
        MERGE (s:Sequence {sequence_id: $sequence_id})
        SET s.source_ip = $source_ip,
            s.start_time = $start_time,
            s.end_time = $end_time
        """,
        sequence_id=sequence_id,
        source_ip=sequence.get("source_ip"),
        start_time=sequence.get("start_time"),
        end_time=sequence.get("end_time")
    ).consume()

    event_ids = []

    for position, event in enumerate(
        sequence.get("events", []),
        start=1
    ):

        event_id = merge_event(tx, event)
        event_ids.append(event_id)

        tx.run(
            """
            MATCH (s:Sequence {sequence_id: $sequence_id})
            MATCH (e:EvidenceEvent {event_id: $event_id})
            MERGE (s)-[r:CONTAINS_EVENT {event_id: $event_id}]->(e)
            SET r.position = $position
            """,
            sequence_id=sequence_id,
            event_id=event_id,
            position=position
        ).consume()

    # Connect consecutive events
    for index in range(len(event_ids) - 1):

        earlier_id = event_ids[index]
        later_id = event_ids[index + 1]

        tx.run(
            """
            MATCH (earlier:EvidenceEvent {event_id: $earlier_id})
            MATCH (later:EvidenceEvent {event_id: $later_id})

            MERGE (earlier)-[r:FOLLOWED_BY {
                sequence_id: $sequence_id
            }]->(later)

            SET r.from_position = $from_position,
                r.to_position = $to_position
            """,
            earlier_id=earlier_id,
            later_id=later_id,
            sequence_id=sequence_id,
            from_position=index + 1,
            to_position=index + 2
        ).consume()


# --------------------------------------------------
# Create correlation relationships
# --------------------------------------------------

def merge_correlation(tx, correlation):

    earlier = correlation["earlier_event"]
    later = correlation["later_event"]

    earlier_id = merge_event(tx, earlier)
    later_id = merge_event(tx, later)

    tx.run(
        """
        MATCH (earlier:EvidenceEvent {event_id: $earlier_id})
        MATCH (later:EvidenceEvent {event_id: $later_id})

        MERGE (earlier)-[r:CORRELATED_WITH {
            rule: $rule
        }]->(later)

        SET r.time_difference_seconds = $time_difference,
            r.reason = $reason
        """,
        earlier_id=earlier_id,
        later_id=later_id,
        rule=correlation["rule"],
        time_difference=correlation.get(
            "time_difference_seconds"
        ),
        reason=correlation.get("reason")
    ).consume()


# --------------------------------------------------
# Create investigation finding nodes
# --------------------------------------------------

def merge_finding(tx, finding):

    sequence_id = finding["sequence_id"]

    properties = {
        "sequence_id": sequence_id,
        "source_ip": finding.get("source_ip"),
        "ml_prediction": finding.get("ml_prediction"),
        "ml_suspicious_probability": finding.get(
            "ml_suspicious_probability"
        ),
        "assessment": finding.get("assessment"),
        "rule_findings_json": json.dumps(
            finding.get("rule_findings", []),
            sort_keys=True
        ),
        "correlated_events_json": json.dumps(
            finding.get("correlated_events", []),
            sort_keys=True
        )
    }

    result = tx.run(
        """
        MATCH (s:Sequence {sequence_id: $sequence_id})

        MERGE (f:InvestigationFinding {
            sequence_id: $sequence_id
        })

        SET f += $properties

        MERGE (s)-[:HAS_FINDING]->(f)

        RETURN f.sequence_id AS sequence_id
        """,
        sequence_id=sequence_id,
        properties=properties
    ).single()

    if result is None:
        raise ValueError(
            f"No matching Sequence found for finding {sequence_id}"
        )


# --------------------------------------------------
# Build complete graph
# --------------------------------------------------

def build_graph_transaction(
    tx,
    evidence,
    sequences,
    correlations,
    hybrid_analysis
):

    for event in evidence:
        merge_event(tx, event)

    for sequence in sequences:
        merge_sequence(tx, sequence)

    for correlation in correlations:
        merge_correlation(tx, correlation)

    for finding in hybrid_analysis:
        merge_finding(tx, finding)


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main():

    print("\nFORENSIC KNOWLEDGE GRAPH BUILDER")
    print("=" * 50)

    print("\nLoading forensic evidence...")

    evidence = load_json(NORMALIZED_EVIDENCE_FILE)
    sequences = load_json(SEQUENCES_FILE)
    correlations = load_json(CORRELATIONS_FILE)
    hybrid_analysis = load_json(HYBRID_ANALYSIS_FILE)

    print(f"Evidence events: {len(evidence)}")
    print(f"Sequences: {len(sequences)}")
    print(f"Correlations: {len(correlations)}")
    print(f"Investigation findings: {len(hybrid_analysis)}")

    password = getpass("\nEnter your Neo4j password: ")

    driver = None

    try:

        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, password)
        )

        driver.verify_connectivity()

        with driver.session(database=NEO4J_DATABASE) as session:

            create_constraints(session)

            session.execute_write(
                build_graph_transaction,
                evidence,
                sequences,
                correlations,
                hybrid_analysis
            )

        print("\nKnowledge graph created successfully!")
        print("Evidence events processed:", len(evidence))
        print("Sequences processed:", len(sequences))
        print("Correlations processed:", len(correlations))
        print("Investigation findings processed:", len(hybrid_analysis))

    except Exception as error:

        print("\nKnowledge graph construction failed.")
        print(f"Error: {error}")

        raise

    finally:

        if driver is not None:
            driver.close()
            print("\nNeo4j connection closed.")


if __name__ == "__main__":
    main()
