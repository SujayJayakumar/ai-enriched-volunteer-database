import os
import time
import json
import requests

# ✅ CORRECT base URL (no {model} here)
HF_API_URL = "https://router.huggingface.co/models/"
HF_TOKEN = os.getenv("HF_API_TOKEN")

USE_LOCAL_FALLBACK = False


class LLMError(Exception):
    pass


def call_llm(prompt_text, model, temperature=0.2, retries=2):
    """
    Unified LLM interface.
    Uses Hugging Face router API.
    """

    if USE_LOCAL_FALLBACK:
        return local_fallback(prompt_text)

    if not HF_TOKEN:
        raise LLMError("HF_API_TOKEN is not set in environment")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt_text,
        "parameters": {
            "temperature": temperature,
            "max_new_tokens": 256,
            "return_full_text": False,
        },
    }

    last_error = None

    for attempt in range(retries + 1):
        try:
            print(f"Calling Hugging Face LLM (attempt {attempt + 1})...")

            response = requests.post(
                HF_API_URL + model,
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code != 200:
                print("HF STATUS:", response.status_code)
                print("HF RESPONSE:", response.text)
                raise LLMError(f"HF error {response.status_code}")

            result = response.json()
            print("HF RAW RESPONSE:", result)

            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]

            raise LLMError("Unexpected HF response format")

        except Exception as e:
            last_error = e
            time.sleep(1)

    raise LLMError(f"HF LLM failed after retries: {last_error}")


def local_fallback(prompt_text):
    """
    Deterministic local enrichment fallback.
    Preserves the same JSON contract as an LLM.
    """
    text = prompt_text.lower()

    skills = []
    if "python" in text:
        skills.append("Python")
    if "options" in text:
        skills.append("Options")
    if "derivatives" in text:
        skills.append("Derivatives")
    if "mentor" in text:
        skills.append("Mentoring")

    if "mentor" in text or "5+ years" in text:
        persona = "Mentor Material"
        confidence = 0.85
    elif "new" in text or "learning" in text:
        persona = "Needs Guidance"
        confidence = 0.75
    else:
        persona = "Passive"
        confidence = 0.6

    return json.dumps({
        "skills": skills,
        "persona": persona,
        "confidence": confidence
    })
