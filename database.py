import sqlite3
from pathlib import Path

DB_PATH = Path("./data/inventory.db")
DB_PATH.parent.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            quantity INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_product(name, code, quantity=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO products (name, code, quantity) VALUES (?, ?, ?)', (name, code, quantity))
    conn.commit()
    conn.close()

def get_product_by_code(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE code=?', (code,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    rows = c.fetchall()
    conn.close()
    return rows
