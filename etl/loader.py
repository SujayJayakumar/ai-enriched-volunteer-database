import csv

REQUIRED_COLUMNS = {
    "member_name",
    "bio_or_comment",
    "last_active_date"
}

def load_csv(path):
    """
    Loads CSV and validates required columns.
    Yields raw rows as dictionaries.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        for idx, row in enumerate(reader, start=1):
            row["_row_id"] = idx
            yield row
