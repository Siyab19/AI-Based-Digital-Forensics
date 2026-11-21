
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
GENERATED_DATA_DIR = DATA_DIR / "generated"

# Model directory
MODEL_DIR = PROJECT_ROOT / "models"

# Raw evidence files
FIREWALL_LOG = RAW_DATA_DIR / "firewall.log"
AUTHENTICATION_LOG = RAW_DATA_DIR / "authentication.log"
BROWSER_HISTORY_LOG = RAW_DATA_DIR / "browser_history.log"

# Generated evidence files
EVIDENCE_FILE = GENERATED_DATA_DIR / "evidence.json"
NORMALIZED_EVIDENCE_FILE = GENERATED_DATA_DIR / "normalized_evidence.json"
EXTRACTED_ENTITIES_FILE = GENERATED_DATA_DIR / "extracted_entities.json"
CORRELATIONS_FILE = GENERATED_DATA_DIR / "correlations.json"
SEQUENCES_FILE = GENERATED_DATA_DIR / "sequences.json"
SEQUENCE_FEATURES_FILE = GENERATED_DATA_DIR / "sequence_features.json"
HYBRID_ANALYSIS_FILE = GENERATED_DATA_DIR / "hybrid_analysis.json"

# ML files
SEQUENCE_TRAINING_DATA = GENERATED_DATA_DIR / "sequence_training_features.json"
SEQUENCE_VALIDATION_DATA = GENERATED_DATA_DIR / "sequence_validation_features.json"
SEQUENCE_MODEL_FILE = MODEL_DIR / "sequence_forensic_model.pkl"
