import datetime
import database

def generate_code(abbr: str, purchase_date: str) -> str:
    """
    Generate LL-ABR-YYMM-#### style code.
    YYMM comes from purchase_date (yyyy-mm-dd),
    counter resets per Gemeinde+month.
    """
    # parse purchase_date -> YYMM
    try:
        dt = datetime.datetime.strptime(purchase_date, "%Y-%m-%d")
    except Exception:
        dt = datetime.date.today()
    year_month = dt.strftime("%y%m")

    # count existing codes for this Gemeinde and month
    conn = database.get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM products WHERE code LIKE ?",
        (f"LL-{abbr.upper()}-{year_month}-%",),
    )
    count = cur.fetchone()[0]
    conn.close()

    seq = count + 1
    return f"LL-{abbr.upper()}-{year_month}-{seq:04d}"


def generate_code1(abbr: str, date, last_number: int) -> str:
    """Generate LL-ABR-YYMM-#### style code."""
    now = datetime.date.today()
    year_month = now.strftime("%y%m")  # %y gives last 2 digits of year, %m gives month as number
    return f"LL-{abbr.upper()}-{year_month}-{last_number:04d}"


def generate_subcodes2(main_code: str, quantity: int) -> list[str]:
    """Generate sequential sub-codes like LL-KUS-2025-11-0001-001."""
    return [f"{main_code}-{i:03d}" for i in range(1, quantity + 1)]