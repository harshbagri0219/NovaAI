import json
import os
import shutil
from datetime import datetime

from memory.models import SCHEMA_VERSION, LEGACY_TO_CATEGORICAL, CATEGORICAL_TO_LEGACY, DEFAULTS

FILE = "database/memory.json"


def backup_memory():
    """Create a backup of the existing memory file before modification.

    - preserves the original file
    - uses a timestamp or unique suffix
    - never silently overwrite an existing backup
    """
    if not os.path.exists(FILE):
        return None

    # Generate unique backup suffix with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = FILE + ".backup_" + timestamp

    # Copy the file with unique name - never silently overwrite
    try:
        shutil.copy2(FILE, backup_file)
        return backup_file
    except Exception:
        return None


def detect_schema_version(data):
    """Detect the schema version of the memory data.

    Returns:
        "0.2.0" if structured format with schema_version field
        "0.1.0" if legacy flat structure (no schema_version field)
        None if data is empty or invalid
    """
    if data is None:
        return None

    if not isinstance(data, dict):
        return None

    # Check for structured schema version
    if SCHEMA_VERSION in data:
        return SCHEMA_VERSION

    # Legacy flat structure - no schema_version field
    return "0.1.0"


def load_memory():
    """Load memory from JSON file with schema detection and error handling.

    - Detects schema version (0.1.0 flat or 0.2.0 structured)
    - Handles missing files gracefully
    - Handles malformed JSON gracefully
    - Returns data compatible with both old and new code
    """
    if not os.path.exists(FILE):
        # Return default structured data for new installations
        return {"schema_version": SCHEMA_VERSION, "data": DEFAULTS.copy()}

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed JSON - return default structured data
        # Do not overwrite the file here; let the caller decide
        return {"schema_version": "0.1.0", "data": {}, "._malformed": True}

    schema_version = detect_schema_version(data)

    if schema_version == SCHEMA_VERSION:
        # Already v0.2 structured format
        return data

    # Legacy v0.1 flat structure - normalize to structured format
    normalized = _migrate_legacy_to_structured(data)
    normalized["schema_version"] = SCHEMA_VERSION
    return normalized


def _migrate_legacy_to_structured(legacy_data):
    """Convert legacy v0.1 flat memory to v0.2 structured format.

    Preserves all existing data without deletion.
    Maps flat keys to structured categories.

    Args:
        legacy_data: dict from v0.1 flat memory.json

    Returns:
        dict with structured format
    """
    if not isinstance(legacy_data, dict):
        return {
            "profile": {},
            "preferences": {},
            "facts": {},
            "conversation": {"recent": [], "summaries": []},
            "tasks": {"active": [], "completed": []},
            "system": {},
        }

    structured = {
        "profile": {},
        "preferences": {},
        "facts": {},
        "conversation": {"recent": [], "summaries": []},
        "tasks": {"active": [], "completed": []},
        "system": {},
    }

    # Map legacy flat keys to structured categories
    for key, value in legacy_data.items():
        if key in LEGACY_TO_CATEGORICAL:
            category, subkey = LEGACY_TO_CATEGORICAL[key]
            structured[category][subkey] = value
        else:
            # Unknown key - store in profile as a generic entry
            if "unknown_" + key not in structured["profile"]:
                structured["profile"]["unknown_" + key] = value

    # Preserve any keys that weren't explicitly mapped
    for key in legacy_data:
        if key not in LEGACY_TO_CATEGORICAL and key not in structured["profile"]:
            structured["profile"][key] = legacy_data[key]

    return structured


def save_memory(data):
    """Save memory data to JSON file with backup and error handling.

    - Creates backup of existing file before overwrite
    - Ensures valid JSON output
    - Handles malformed data gracefully
    - Maintains offline-first operation

    Args:
        data: dict to save to memory.json

    Returns:
        True if save successful, False otherwise
    """
    # Ensure data has schema_version
    if not isinstance(data, dict):
        return False

    if "schema_version" not in data:
        data["schema_version"] = SCHEMA_VERSION

    # Create backup of existing file before modifying
    backup_path = backup_memory()

    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except (OSError, TypeError) as e:
        # Attempt to restore from backup on failure
        if backup_path and os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, FILE)
            except Exception:
                pass
        return False
      