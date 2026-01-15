import os
import json
from groq import Groq

class LLMError(Exception):
    pass


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_groq(prompt_text, model, temperature):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a careful data extraction assistant."},
                {"role": "user", "content": prompt_text},
            ],
            temperature=temperature,
        )

        content = response.choices[0].message.content
        return content

    except Exception as e:
        raise LLMError(str(e))
