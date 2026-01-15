import os
from groq import Groq


class LLMError(Exception):
    pass


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise LLMError("GROQ_API_KEY is not set")
    return Groq(api_key=api_key)


def call_groq(prompt_text, model, temperature=0.2):
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content
