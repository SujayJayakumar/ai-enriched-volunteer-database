import json
from datetime import datetime

def log_error(row_id, field, value, reason, file="etl_errors.log"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "row_id": row_id,
        "field": field,
        "value": value,
        "reason": reason
    }

    with open(file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
