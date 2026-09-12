from src.llm.extractor import extract_information


text = """
OpenAI is an artificial intelligence research and deployment company.
It develops advanced AI models and tools for developers and businesses.
"""


result = extract_information(
    text,
    "https://example.com/openai"
)

print("\nFinal result:")
print(result)