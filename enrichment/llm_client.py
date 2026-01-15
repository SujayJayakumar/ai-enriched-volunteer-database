import json
from enrichment.groq_client import call_groq, LLMError

USE_LOCAL_FALLBACK = False


def call_llm(prompt_text, model, temperature=0.2, retries=1, provider="groq"):
    """
    Unified LLM interface.

    Default behavior:
    - Use Groq as the primary LLM provider
    - Fall back to deterministic local logic only if Groq fails
    """

    if provider != "groq":
        raise LLMError(f"Unsupported LLM provider: {provider}")

    try:
        return call_groq(
            prompt_text=prompt_text,
            model=model,
            temperature=temperature,
        )

    except Exception as e:
        if USE_LOCAL_FALLBACK:
            return local_fallback(prompt_text)
        raise LLMError(f"Groq LLM failed: {e}")


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

    if "mentor" in text and "years" in text:
        persona = "Mentor Material"
        confidence = 0.85
    elif "learning" in text or "new" in text:
        persona = "Needs Guidance"
        confidence = 0.55
    else:
        persona = "Passive"
        confidence = 0.5

    return json.dumps({
        "skills": skills,
        "persona": persona,
        "confidence": confidence
    })
