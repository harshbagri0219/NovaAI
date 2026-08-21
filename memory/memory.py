import json
import os
import shutil
from datetime import datetime

from memory.models import (
    SCHEMA_VERSION,
    LEGACY_TO_CATEGORICAL,
    DEFAULTS,
)

FILE = "database/memory.json"


def backup_memory():
    """Create a unique backup of the existing memory file."""
    if not os.path.exists(FILE):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = FILE + ".backup_" + timestamp

    try:
        shutil.copy2(FILE, backup_file)
        return backup_file
    except (OSError, shutil.Error):
        return None


def detect_schema_version(data):
    """Detect the memory schema version."""
    if data is None or not isinstance(data, dict):
        return None

    if data.get("schema_version") == SCHEMA_VERSION:
        return SCHEMA_VERSION

    return "0.1.0"


def load_memory():
    """Load memory using the canonical v0.2 structure."""

    if not os.path.exists(FILE):
        return {
            "schema_version": SCHEMA_VERSION,
            "data": _default_data(),
        }

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return {
            "schema_version": SCHEMA_VERSION,
            "data": _default_data(),
        }

    schema_version = detect_schema_version(data)

    if schema_version == SCHEMA_VERSION:

        # Already canonical v0.2.
        # Do not migrate or transform it again.

        if isinstance(data.get("data"), dict):
            return data

        # Repair malformed v0.2 wrapper without
        # interpreting its contents as legacy data.
        return {
            "schema_version": SCHEMA_VERSION,
            "data": _default_data(),
        }

    # Legacy v0.1 data.
    normalized = _migrate_legacy_to_structured(data)

    return {
        "schema_version": SCHEMA_VERSION,
        "data": normalized,
    }


def _default_data():
    """Return a fresh copy of the default memory structure."""

    return {
        "profile": {},
        "preferences": {},
        "facts": {},
        "conversation": {
            "recent": [],
            "summaries": [],
        },
        "tasks": {
            "active": [],
            "completed": [],
        },
        "system": {},
    }


def _migrate_legacy_to_structured(legacy_data):
    """Convert legacy v0.1 flat memory into canonical v0.2 data.

    This function only migrates genuinely flat legacy data.
    It never recursively wraps already-structured data.
    """

    structured = _default_data()

    if not isinstance(legacy_data, dict):
        return structured

    for key, value in legacy_data.items():

        # Ignore schema metadata.
        if key == "schema_version":
            continue

        # Known legacy keys.
        if key in LEGACY_TO_CATEGORICAL:
            category, subkey = LEGACY_TO_CATEGORICAL[key]

            if category not in structured:
                structured[category] = {}

            if isinstance(structured[category], dict):
                structured[category][subkey] = value

            continue

        # Preserve unknown legacy values in profile.
        # Do NOT prepend "unknown_" repeatedly.
        if key not in structured["profile"]:
            structured["profile"][key] = value

    return structured


def save_memory(data):
    """Save canonical memory data safely.

    Creates a backup before replacing the existing memory file.
    """

    if not isinstance(data, dict):
        return False

    # Ensure canonical schema metadata.
    data["schema_version"] = SCHEMA_VERSION

    # Ensure canonical data wrapper.
    if not isinstance(data.get("data"), dict):
        data["data"] = _default_data()

    # Create database directory before backup/save.
    os.makedirs(os.path.dirname(FILE), exist_ok=True)

    # IMPORTANT:
    # backup_path must be created before attempting to save.
    backup_path = backup_memory()

    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return True

    except (OSError, TypeError, ValueError):

        # Restore previous database if saving failed.
        if backup_path and os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, FILE)
            except (OSError, shutil.Error):
                pass

        return False