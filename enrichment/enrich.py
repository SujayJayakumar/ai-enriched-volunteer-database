import os
import json
import yaml
from datetime import datetime

from enrichment.llm_client import call_llm, LLMError
from db.models import get_connection


def load_prompt(prompt_version):
    base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(base_dir, "prompts.yaml")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f)

    if prompt_version not in prompts:
        raise ValueError(f"Unknown prompt version: {prompt_version}")

    return prompts[prompt_version]


def enrich_member(member_id, bio, config):
    prompt_cfg = load_prompt(config["enrichment"]["prompt_version"])

    prompt_text = (
        prompt_cfg["system"]
        + "\n\n"
        + prompt_cfg["user"].replace("{{bio}}", bio)
    )

    try:
        raw = call_llm(
            prompt_text=prompt_text,
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            retries=config["enrichment"]["retry_attempts"],
        )
    except Exception as e:
        # CRITICAL DEBUG LOG
        print("LLM ERROR:", e)
        return False

    # Log raw output BEFORE parsing
    print("Raw LLM output:", raw)

    try:
        data = json.loads(raw)
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        print("RAW TEXT WAS:", raw)
        return False

    # -------------------------------
    # ✅ NORMALIZATION & SAFETY LOGIC
    # -------------------------------

    persona = data.get("persona")

    # Cap confidence to avoid absolute certainty
    confidence = min(float(data.get("confidence", 0)), 0.95)

    # Normalize skills (clean casing, remove noise)
    raw_skills = data.get("skills", [])
    skills = [
        s.strip().title()
        for s in raw_skills
        if isinstance(s, str) and s.strip()
    ]

    # Low-confidence flagging
    if confidence < config["llm"]["confidence_threshold"]:
        persona = "Uncertain"

    persist_enrichment(
        member_id,
        persona,
        confidence,
        skills,
        config["llm"]["model"],
        config["enrichment"]["prompt_version"],
    )

    return True


def persist_enrichment(
    member_id, persona, confidence, skills, model_version, prompt_version
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO persona_analysis (
            member_id, persona, confidence, model_version, created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            member_id,
            persona,
            confidence,
            model_version,
            datetime.utcnow().isoformat(),
        ),
    )

    for skill in skills:
        cursor.execute(
            "INSERT OR IGNORE INTO skills (skill_name) VALUES (?)",
            (skill,),
        )

        cursor.execute(
            "SELECT skill_id FROM skills WHERE skill_name = ?",
            (skill,),
        )
        skill_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT OR REPLACE INTO member_skills (
                member_id, skill_id, source, confidence
            )
            VALUES (?, ?, ?, ?)
            """,
            (member_id, skill_id, "llm", confidence),
        )

    conn.commit()
    conn.close()
