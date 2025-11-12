import pandas as pd
from pathlib import Path
import json
import database
from utils import generate_code


# === CONFIGURATION ===
EXCEL_PATH = Path("./data/Inventar_2025.xlsx")   # 👈 update this path
SHEET_NAME = "table2"                                         # or the sheet name, e.g. "Inventar"
GEMEINDEN_PATH = Path("./data/gemeinden.json")           # same file used by app


def normalize_value(v):
    """Convert NaN/None/empty to None or stripped string."""
    if pd.isna(v):
        return None
    if isinstance(v, str):
        v = v.strip()
        return v if v else None
    return v


def import_excel():
    if not EXCEL_PATH.exists():
        print(f"❌ Excel file not found at {EXCEL_PATH}")
        return

    if not GEMEINDEN_PATH.exists():
        print(f"❌ Gemeindeliste not found at {GEMEINDEN_PATH}")
        return

    # Load abbreviation map
    with open(GEMEINDEN_PATH, "r", encoding="utf-8") as f:
        gdata = json.load(f)

    abbr_map = {**gdata["VGs"], **gdata["Gemeinden"]}

    print(f"📥 Reading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, engine="openpyxl")

    column_map = {
        "Gemeinde": "gemeinde",
        "Einsatzort": "einsatzort",
        "Kategorie": "kategorie",
        "Produkttyp": "produkttyp",
        "Produktdetails": "produktdetails",
        "Anzahl": "anzahl",
        "Hersteller": "hersteller",
        "Bezugsquelle / Lieferant": "lieferant",
        "ggfs. Link zum Shop": "shop_link",
        "Einzelpreis / netto (Website)": "preis_netto",
        "Einzelpreis / brutto": "preis_brutto",
        "Bestellt": "bestellt_am",
        "Geliefert": "geliefert_am",
        "Bezahlt": "bezahlt",
        "Übergeben": "uebergeben_am",
        "Subproject": "projekt",
        "Bemerkungen": "bemerkungen"
    }

    imported = 0
    total_rows = len(df)

    for _, row in df.iterrows():
        data = {}
        for excel_col, db_field in column_map.items():
            if excel_col in df.columns:
                data[db_field] = normalize_value(row[excel_col])

        # Skip rows completely empty
        if not any(data.values()):
            continue

        gemeinde = data.get("gemeinde")
        if not gemeinde:
            continue

        # Find abbreviation (case-insensitive)
        abbr = None
        for name, a in abbr_map.items():
            if name.lower().strip() == gemeinde.lower().strip():
                abbr = a
                break

        if not abbr:
            abbr = gemeinde[:3].upper()  # fallback if not found

        # Generate code consistently
        current_total = len(database.get_all_products()) + 1
        data["code"] = generate_code(abbr, current_total)

        # Fill defaults
        data.setdefault("anzahl", 1)
        data.setdefault("bezahlt", "Nein")

        try:
            database.add_product_safe(**data)
            imported += 1
        except Exception as e:
            print(f"⚠️ Error importing {gemeinde}: {e}")

    print(f"✅ Imported {imported}/{total_rows} rows successfully.")


if __name__ == "__main__":
    import_excel()
