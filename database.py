import sqlite3
from pathlib import Path

DB_PATH = Path("data/inventory.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            purchase_date TEXT,
            assigned_to TEXT,
            sub_project TEXT,
            storage_location TEXT,
            value REAL,
            remarks TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_product_safe(**kwargs):
    """Insert product inside a transaction."""
    conn = get_connection()
    try:
        with conn:  # ensures commit/rollback automatically
            fields = ", ".join(kwargs.keys())
            placeholders = ", ".join(["?"] * len(kwargs))
            values = tuple(kwargs.values())
            conn.execute(f"INSERT INTO products ({fields}) VALUES ({placeholders})", values)
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_product_by_code(code):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE code=?", (code,))
    row = c.fetchone()
    conn.close()
    return row
