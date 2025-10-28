import datetime
import database

def generate_code(location_abbr: str) -> str:
    """Generate code like LL-ALB-2025-00001"""
    year = datetime.date.today().year
    prefix = f"LL-{location_abbr.upper()}-{year}-"
    all_items = database.get_all_products()
    number = len(all_items) + 1
    return f"{prefix}{number:05d}"
