Volunteer Shadow Source of Truth System

This project implements a Volunteer-First Operating System with a focus on building a Shadow Source of Truth from noisy, human-generated data. It demonstrates how deterministic data processing and probabilistic AI enrichment can coexist in a reliable, auditable system.

The system ingests raw member data, normalizes it, enriches it using an AI layer, persists structured outputs in a normalized database, and exposes a queryable CLI interface designed for real-world decision-making.


-------------------------------------

Project Goals

Convert messy, human-generated volunteer data into a structured, queryable database

Enrich unstructured text (bios/comments) using AI

Preserve traceability, confidence, and versioning of AI outputs

Design for change, reprocessing, and uncertainty

Demonstrate engineering judgment under real-world constraints

--------------------------------------------

System Architecture

The system is divided into four explicit layers, each with a single responsibility.

Raw CSV
  ↓
ETL Layer (Deterministic)
  ↓
Truth Layer (SQLite)
  ↓
AI Enrichment Layer (Probabilistic)
  ↓
Query & CLI Interface


ETL Layer (Ingest & Normalize)

Purpose:
Transform noisy CSV data into clean, validated records without guessing or hallucinating.

Key characteristics:

Modular pipeline (loader, normalizer, logger)

Name normalization and date standardization

Invalid fields are flagged and logged, not silently fixed

No AI used at this stage

Why this design:
AI should never be the first line of defense. Deterministic normalization ensures a stable foundation before enrichment.


Truth Layer (Persistence & Data Modeling)

Database: SQLite (data/volunteer_data.db)

Core tables:

members – canonical volunteer records

skills – normalized skill dictionary

member_skills – many-to-many relationship

persona_analysis – AI-derived personas with confidence

enrichment_runs – metadata for enrichment executions

Key design choices:

Fully normalized schema

Idempotent enrichment (no duplicate skills)

AI outputs stored alongside model version and timestamp

Supports safe re-runs and future model comparisons

Why SQLite:
Lightweight, portable, and sufficient for demonstrating relational modeling and query design.


AI Enrichment Layer (Brain)

Purpose:
Extract structured insights from unstructured bio_or_comment text.

What the AI extracts

Skills (as structured, queryable data)

Persona classification

Mentor Material

Needs Guidance

Passive

Confidence score (0–1)

--------------------------------------------

Prompting Strategy (Config-Driven)

Prompts are not hard-coded.

Stored in enrichment/prompts.yaml

Selected via config.yaml

Versioned (e.g. persona_v1)

Example prompt design:

Strict instructions

Explicit JSON schema

No speculation beyond the text

Model-agnostic (works across providers)

This allows:

Prompt iteration without code changes

A/B testing in future

Clean separation of logic and language

--------------------------------------------


Confidence & Uncertainty Handling

A global confidence threshold of 0.6 is enforced (configured in config.yaml).

llm:
  confidence_threshold: 0.6


If an AI output falls below this threshold:

The persona is flagged as Uncertain

Data is still stored (not discarded)

Downstream systems can decide how to treat it

This avoids unsafe automation while preserving traceability.

--------------------------------------------

LLM Provider Strategy & Reliability

During development, Hugging Face hosted inference was tested via both:

Legacy inference endpoint

Router-based endpoint

These attempts surfaced:

Endpoint deprecation

404 / 503 errors under free-tier constraints

Rather than silently failing or blocking the system, the enrichment layer was designed to gracefully degrade via a deterministic fallback model that:

Preserves the same JSON contract

Maintains confidence handling

Keeps the pipeline fully functional for demonstration and evaluation

The abstraction allows switching back to a live LLM provider (e.g. Groq, OpenAI) without refactoring.

--------------------------------------------

Query & CLI Interface

A minimal command-line interface is provided to demonstrate real value extraction.

Example use case

“Show potential mentors, ranked by confidence and recent activity.”

Run the CLI
python cli.py --mentors --limit 5

With uncertainty warnings enabled
python cli.py --mentors --limit 5 --warn-uncertain


If a persona is marked as Uncertain, the CLI emits a clear warning:

⚠️  Warning: Low-confidence AI classification. Human review recommended.


This makes AI uncertainty explicit to the user, supporting responsible decision-making.

--------------------------------------------

How to Run the System
1. Set up environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Run the pipeline
python main.py


3. Query results
python cli.py --mentors --warn-uncertain

--------------------------------------------

Assumptions & Limitations

City/location filtering can be added once reliable location data is available

Free-tier hosted LLMs may be unstable; fallback ensures reproducibility

Confidence scores are model-relative, not absolute truth

