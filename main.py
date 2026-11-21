
from src.config import (
    FIREWALL_LOG,
    AUTHENTICATION_LOG,
    BROWSER_HISTORY_LOG,
    SEQUENCE_MODEL_FILE
)

from src.ingestion.log_parser import main as run_log_parser
from src.preprocessing.normalizer import main as run_normalizer
from src.preprocessing.entity_extractor import main as run_entity_extractor
from src.correlation.correlator import main as run_correlator
from src.sequence.sequence_builder import main as run_sequence_builder
from src.sequence.sequence_feature_extractor import main as run_feature_extractor
from src.ml.sequence_model_predictor import main as run_sequence_predictor
from src.analysis.hybrid_analyzer import main as run_hybrid_analyzer


def validate_project():
    """Check whether the required input files and trained model exist."""

    required_files = [
        FIREWALL_LOG,
        AUTHENTICATION_LOG,
        BROWSER_HISTORY_LOG,
        SEQUENCE_MODEL_FILE
    ]

    missing_files = [
        file for file in required_files
        if not file.exists()
    ]

    if missing_files:
        print("\nPipeline cannot start. Missing required files:")

        for file in missing_files:
            print(f"- {file}")

        if not SEQUENCE_MODEL_FILE.exists():
            print(
                "\nTrain the model first using:\n"
                "python -m src.ml.sequence_ml_model"
            )

        return False

    return True


def run_step(step_name, function):
    """Execute one pipeline stage."""

    print("\n" + "=" * 60)
    print(f"RUNNING: {step_name}")
    print("=" * 60)

    function()

    print(f"\nCOMPLETED: {step_name}")


def main():

    print("\nAI-BASED DIGITAL FORENSICS AND EVIDENCE CORRELATION")
    print("=" * 60)

    if not validate_project():
        return

    pipeline_steps = [
        ("Log Parsing", run_log_parser),
        ("Evidence Normalization", run_normalizer),
        ("Entity Extraction", run_entity_extractor),
        ("Deterministic Evidence Correlation", run_correlator),
        ("Sequence Construction", run_sequence_builder),
        ("Sequence Feature Extraction", run_feature_extractor),
        ("Sequence-Level ML Prediction", run_sequence_predictor),
        ("Hybrid Evidence Analysis", run_hybrid_analyzer)
    ]

    try:
        for step_name, function in pipeline_steps:
            run_step(step_name, function)

    except Exception as error:
        print("\nPIPELINE FAILED")
        print(f"Error: {error}")
        raise

    print("\n" + "=" * 60)
    print("FORENSIC ANALYSIS PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nFinal output:")
    print("data/generated/hybrid_analysis.json")


if __name__ == "__main__":
    main()
