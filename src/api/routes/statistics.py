from fastapi import APIRouter, Depends, HTTPException
from neo4j import Session

from src.api.database import get_session


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.get("/")
def get_statistics(
    session: Session = Depends(get_session)
):
    """Retrieve overall forensic investigation statistics."""

    try:
        investigation_query = """
        MATCH (s:Sequence)-[:HAS_FINDING]->(f:InvestigationFinding)

        RETURN
            count(s) AS total_investigations,

            sum(
                CASE WHEN f.assessment = 'requires_investigation'
                THEN 1 ELSE 0 END
            ) AS requires_investigation,

            sum(
                CASE WHEN f.assessment = 'correlated_activity_observed'
                THEN 1 ELSE 0 END
            ) AS correlated_activity_observed,

            sum(
                CASE WHEN f.assessment = 'no_significant_finding'
                THEN 1 ELSE 0 END
            ) AS no_significant_finding,

            sum(
                CASE WHEN f.ml_prediction = 'suspicious'
                THEN 1 ELSE 0 END
            ) AS suspicious_predictions,

            sum(
                CASE WHEN f.ml_prediction = 'normal'
                THEN 1 ELSE 0 END
            ) AS normal_predictions,

            avg(f.ml_suspicious_probability) AS average_suspicious_score
        """

        investigation_record = session.run(
            investigation_query
        ).single()

        evidence_query = """
        MATCH (e:EvidenceEvent)
        RETURN count(e) AS total_evidence_events
        """

        evidence_record = session.run(
            evidence_query
        ).single()

        correlation_query = """
        MATCH ()-[r:CORRELATED_WITH]->()
        RETURN count(r) AS total_correlations
        """

        correlation_record = session.run(
            correlation_query
        ).single()

        return {
            "total_investigations": investigation_record["total_investigations"],
            "total_evidence_events": evidence_record["total_evidence_events"],
            "total_correlations": correlation_record["total_correlations"],
            "requires_investigation": investigation_record["requires_investigation"] or 0,
            "correlated_activity_observed": investigation_record["correlated_activity_observed"] or 0,
            "no_significant_finding": investigation_record["no_significant_finding"] or 0,
            "suspicious_predictions": investigation_record["suspicious_predictions"] or 0,
            "normal_predictions": investigation_record["normal_predictions"] or 0,
            "average_suspicious_score": investigation_record["average_suspicious_score"] or 0
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve statistics: {str(error)}"
        )