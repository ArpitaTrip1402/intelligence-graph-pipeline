import re


# Deterministic aliases
ENTITY_ALIASES = {
    "openai": "OpenAI",
    "open ai": "OpenAI",
    "openai inc": "OpenAI",
    "openai inc.": "OpenAI",

    "google deepmind": "Google DeepMind",
    "deepmind": "Google DeepMind",

    "microsoft": "Microsoft",
    "microsoft corp": "Microsoft",

    "meta": "Meta",
    "meta platforms": "Meta",
}


def normalize_entity(name):
    """
    Normalize an entity name before matching.
    """

    if not name:
        return None

    name = name.lower().strip()

    # Remove punctuation
    name = re.sub(r"[^\w\s]", "", name)

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name)

    return name


def resolve_entity(name):
    """
    Convert different forms of an entity
    into one canonical name.
    """

    normalized = normalize_entity(name)

    if normalized in ENTITY_ALIASES:
        canonical = ENTITY_ALIASES[normalized]
    else:
        # If no known alias exists, preserve the original name.
        canonical = name.strip()

    return canonical


def create_mapping_record(raw_entity, entity_type):
    """
    Create a record for the Entity Mapping Log.
    """

    canonical_entity = resolve_entity(raw_entity)

    if canonical_entity == raw_entity.strip():
        reason = "No alias mapping required"
    else:
        reason = "Deterministic alias mapping"

    return {
        "raw_entity": raw_entity,
        "canonical_entity": canonical_entity,
        "entity_type": entity_type,
        "reason": reason
    }