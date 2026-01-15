from datetime import datetime
from dateutil import parser

def normalize_name(name):
    if not name or not name.strip():
        return None
    return name.strip().title()

def normalize_city(city):
    if not city or not city.strip():
        return None
    return city.strip().title()

def normalize_date(date_str):
    if not date_str or not date_str.strip():
        return None
    try:
        parsed = parser.parse(date_str, dayfirst=True, fuzzy=True)
        return parsed.date().isoformat()
    except Exception:
        return None
