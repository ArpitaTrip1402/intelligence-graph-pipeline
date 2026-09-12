import os
import time
import random
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def truncate_text(text, max_chars=12000):
    """
    Keep the input within a reasonable size for the LLM.
    """
    if len(text) <= max_chars:
        return text

    return text[:max_chars]


def call_with_retry(client, model, prompt, max_retries=3):
    """
    Call an LLM with exponential backoff for rate-limit errors.
    """

    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"{model} failed:", e)

            if attempt == max_retries - 1:
                return None

            # Exponential backoff + jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)

            print(f"Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)

    return None

def parse_json_response(result):
    if not result:
        return None

    result = result.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        print("Invalid JSON returned by LLM.")
        return None


def extract_information(text, source_url):

    text = truncate_text(text)

    prompt = f"""
Extract structured information from the following source.

Return ONLY valid JSON.

Required fields:

{{
    "name": "",
    "description": "",
    "source_url": "{source_url}"
}}

Source text:

{text}
"""

    # --------------------------------------------------
    # 1. Gemini
    # --------------------------------------------------

    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:

        print("Trying Gemini...")

        gemini_client = OpenAI(
            api_key=gemini_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        result = call_with_retry(
            gemini_client,
            "gemini-3.6-flash",
            prompt
        )

        parsed = parse_json_response(result)

        if parsed:
         return parsed

    # --------------------------------------------------
    # 2. Groq
    # --------------------------------------------------

    groq_key = os.getenv("GROQ_API_KEY")

    if groq_key:

        print("Trying Groq...")

        groq_client = OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1"
        )

        result = call_with_retry(
            groq_client,
            "openai/gpt-oss-120b",
            prompt
        )

        parsed = parse_json_response(result)

        if parsed:
          return parsed

       

    # --------------------------------------------------
    # 3. DeepSeek
    # --------------------------------------------------

    deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    if deepseek_key:

        print("Trying DeepSeek...")

        deepseek_client = OpenAI(
            api_key=deepseek_key,
            base_url="https://api.deepseek.com"
        )

        result = call_with_retry(
            deepseek_client,
            "deepseek-chat",
            prompt
        )

        parsed = parse_json_response(result)

        if parsed:
          return parsed

        

    print("All LLM providers failed.")

    return None