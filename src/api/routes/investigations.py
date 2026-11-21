
import json

from fastapi import APIRouter, Depends, HTTPException
from neo4j import Session

from src.api.database import get_session


router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"]
)


def parse_json_field(value):
    """Convert stored JSON strings into Python objects."""
    if not value:
        return []

    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


def fetch_investigations(session: Session):
    """Retrieve investigation findings and associated evidence details."""

    query = """
    MATCH (s:Sequence)-[:HAS_FINDING]->(f:InvestigationFinding)

    OPTIONAL MATCH (s)-[:CONTAINS_EVENT]->(e:EvidenceEvent)
    OPTIONAL MATCH (e)-[:INVOLVES_USER]->(u:User)
    OPTIONAL MATCH (e)-[:ORIGINATED_FROM]->(ip:IPAddress)

    WITH
        s,
        f,
        count(DISTINCT e) AS event_count,
        [value IN collect(DISTINCT u.name)
            WHERE value IS NOT NULL] AS users,
        [value IN collect(DISTINCT ip.address)
            WHERE value IS NOT NULL] AS source_ips

    RETURN
        s.sequence_id AS sequence_id,
        head(users) AS user,
        head(source_ips) AS source_ip,
        event_count AS event_count,
        f.assessment AS assessment,
        f.ml_prediction AS ml_prediction,
        f.ml_suspicious_probability AS suspicious_score,
        f.rule_findings_json AS rule_findings_json,
        f.correlated_events_json AS correlated_events_json

    ORDER BY s.sequence_id
    """

    result = session.run(query)

    investigations = []

    for record in result:
        investigations.append({
            "sequence_id": record["sequence_id"],
            "user": record["user"] or "Unknown",
            "source_ip": record["source_ip"],
            "event_count": record["event_count"],
            "assessment": record["assessment"],
            "ml_prediction": record["ml_prediction"],
            "suspicious_score": record["suspicious_score"],
            "rule_findings": parse_json_field(
                record["rule_findings_json"]
            ),
            "correlated_events": parse_json_field(
                record["correlated_events_json"]
            )
        })

    return investigations


@router.get("/")
def get_investigations(
    session: Session = Depends(get_session)
):
    """Return all forensic investigation findings."""

    try:
        investigations = fetch_investigations(session)

        return {
            "total_investigations": len(investigations),
            "investigations": investigations
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve investigations: {str(error)}"
        )

@router.get("/{sequence_id}")
def get_investigation_details(
    sequence_id: int,
    session: Session = Depends(get_session)
):
    """Retrieve the complete details of one investigation."""

    query = """
    MATCH (s:Sequence {sequence_id: $sequence_id})

    OPTIONAL MATCH (s)-[:HAS_FINDING]->(f:InvestigationFinding)

    OPTIONAL MATCH (s)-[r:CONTAINS_EVENT]->(e:EvidenceEvent)
    OPTIONAL MATCH (e)-[:INVOLVES_USER]->(u:User)
    OPTIONAL MATCH (e)-[:ORIGINATED_FROM]->(ip:IPAddress)
    OPTIONAL MATCH (e)-[:OBSERVED_ON]->(d:Device)

    WITH s, f, e, r, u, ip, d
    ORDER BY r.position

    RETURN
        s.sequence_id AS sequence_id,
        f.assessment AS assessment,
        f.ml_prediction AS ml_prediction,
        f.ml_suspicious_probability AS suspicious_score,
        f.rule_findings_json AS rule_findings_json,
        f.correlated_events_json AS correlated_events_json,

        collect(
            CASE WHEN e IS NULL THEN null
            ELSE {
                position: r.position,
                timestamp: e.timestamp,
                source: e.source,
                event_type: e.event_type,
                action: e.action,
                status: e.status,
                user: u.name,
                source_ip: ip.address,
                device: d.name,
                destination_ip: e.destination_ip,
                resource: e.resource
            }
            END
        ) AS evidence_timeline
    """

    try:
        result = session.run(
            query,
            sequence_id=sequence_id
        )

        record = result.single()

        if record is None:
            raise HTTPException(
                status_code=404,
                detail=f"Investigation {sequence_id} not found."
            )

        return {
            "sequence_id": record["sequence_id"],
            "assessment": record["assessment"],
            "ml_prediction": record["ml_prediction"],
            "suspicious_score": record["suspicious_score"],
            "rule_findings": parse_json_field(
                record["rule_findings_json"]
            ),
            "correlated_events": parse_json_field(
                record["correlated_events_json"]
            ),
            "evidence_timeline": record["evidence_timeline"]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve investigation: {str(error)}"
        )

@router.get("/{sequence_id}/correlations")
def get_investigation_correlations(
    sequence_id: int,
    session: Session = Depends(get_session)
):
    """Retrieve correlated evidence events for one sequence."""

    query = """
    MATCH (s:Sequence {sequence_id: $sequence_id})

    MATCH (s)-[:CONTAINS_EVENT]->(earlier:EvidenceEvent)
          -[r:CORRELATED_WITH]->
          (later:EvidenceEvent)<-[:CONTAINS_EVENT]-(s)

    RETURN
        r.rule AS rule,
        r.reason AS explanation,
        r.time_difference_seconds AS time_difference_seconds,
        properties(earlier) AS earlier_event,
        properties(later) AS later_event

    ORDER BY earlier.timestamp
    """

    try:
        result = session.run(
            query,
            sequence_id=sequence_id
        )

        correlations = []

        for record in result:
            correlations.append({
                "rule": record["rule"],
                "explanation": record["explanation"],
                "time_difference_seconds": (
                    record["time_difference_seconds"]
                ),
                "earlier_event": record["earlier_event"],
                "later_event": record["later_event"]
            })

        return {
            "sequence_id": sequence_id,
            "total_correlations": len(correlations),
            "correlations": correlations
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve correlations: {str(error)}"
        )
