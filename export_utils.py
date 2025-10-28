import csv
from pathlib import Path
import database

EXPORT_PATH = Path("./data/inventory_export.csv")

def export_to_csv():
    rows = database.get_all_products()
    header = ["id", "name", "code", "purchase_date", "assigned_to",
              "sub_project", "storage_location", "value", "remarks"]
    with open(EXPORT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    return EXPORT_PATH
