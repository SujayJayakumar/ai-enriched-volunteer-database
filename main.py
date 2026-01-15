from etl.loader import load_csv
from etl.normalizer import normalize_name, normalize_date
from etl.logger import log_error
from db.models import initialize_db, insert_member
from enrichment.enrich import enrich_member

import yaml


def run_etl(csv_path):
    cleaned_rows = []

    for row in load_csv(csv_path):
        row_id = row["_row_id"]

        name = normalize_name(row.get("member_name"))
        if name is None:
            log_error(
                row_id,
                "member_name",
                row.get("member_name"),
                "Invalid or empty name",
            )

        last_active = normalize_date(row.get("last_active_date"))
        if last_active is None and row.get("last_active_date"):
            log_error(
                row_id,
                "last_active_date",
                row.get("last_active_date"),
                "Invalid date",
            )

        cleaned_rows.append(
            {
                "row_id": row_id,
                "name": name,
                "last_active": last_active,
                "bio": row.get("bio_or_comment", "").strip(),
            }
        )

    return cleaned_rows


def main():
    # Load config
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Initialize DB + schema
    initialize_db()

    # ETL
    rows = run_etl("data/members_raw.csv")

    # Insert truth + capture DB IDs
    member_rows = []
    for row in rows:
        member_id = insert_member(row)
        member_rows.append((member_id, row))

    # AI enrichment (LIMITED for free-tier safety)
    MAX_ENRICH = 1  

    # AI enrichment
    for i, (member_id, row) in enumerate(member_rows, start=1):
        print(f"Enriching member {i}/{len(member_rows)}...")
        enrich_member(member_id, row["bio"], config)

    print(f"Ingested and enriched {len(member_rows)} members.")



if __name__ == "__main__":
    main()
    
