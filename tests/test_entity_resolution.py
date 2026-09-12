from src.pipeline.entity_resolution import (
    resolve_entity,
    create_mapping_record
)


entities = [
    "OpenAI",
    "Open AI",
    "OpenAI Inc.",
    "DeepMind",
    "Google DeepMind",
    "Microsoft",
    "Unknown Company"
]


for entity in entities:

    canonical = resolve_entity(entity)

    print(
        f"{entity} -> {canonical}"
    )


print("\nMapping log example:")

record = create_mapping_record(
    "Open AI",
    "COMPANY"
)

print(record)