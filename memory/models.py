# NOVA v0.2 Memory Models
# Schema version and data model definitions for structured memory

SCHEMA_VERSION = "0.2.0"

# Canonical memory categories
CATEGORIES = {
    "profile": "User profile information (name, location, preferences)",
    "preferences": "User preferences (likes, dislikes, communication style)",
    "facts": "Learned facts and information",
    "conversation": "Conversation history and summaries",
    "tasks": "Task tracking and status",
    "system": "System and device information",
}

# Legacy key → structured category mapping
LEGACY_TO_CATEGORICAL = {
    # Profile legacy keys → profile category
    "owner": ("profile", "owner"),
    "location": ("profile", "location"),
    "favorite_language": ("profile", "favorite_language"),
    "favorite_food": ("profile", "favorite_food"),
    "languages": ("profile", "languages"),
    
    # Preference legacy keys → preferences category
    # (no direct legacy flat keys for preferences in v0.1, but reserved for future)
}

# Reverse mapping: structured category → legacy key
CATEGORICAL_TO_LEGACY = {v[1]: k for k, v in LEGACY_TO_CATEGORICAL.items()}

# Default values for each category when creating new memory
DEFAULTS = {
    "profile": {},
    "preferences": {},
    "facts": {},
    "conversation": {"recent": [], "summaries": []},
    "tasks": {"active": [], "completed": []},
    "system": {},
}