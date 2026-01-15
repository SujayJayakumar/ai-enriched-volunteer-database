CREATE TABLE IF NOT EXISTS members (
  member_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  city TEXT,
  join_date DATE,
  last_active DATE,
  ingestion_ts TIMESTAMP,
  status TEXT
);

CREATE TABLE IF NOT EXISTS skills (
  skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
  skill_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS member_skills (
  member_id INTEGER,
  skill_id INTEGER,
  source TEXT,
  confidence REAL,
  PRIMARY KEY (member_id, skill_id)
);

CREATE TABLE IF NOT EXISTS persona_analysis (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id INTEGER,
  persona TEXT,
  confidence REAL,
  model_version TEXT,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS enrichment_runs (
  run_id TEXT,
  model_name TEXT,
  prompt_version TEXT,
  created_at TIMESTAMP
);
