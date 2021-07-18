DATABASE_PATH = "../data/data.db"  # from app.py location
TABLE_ITEMS = "items"
TABLE_USERS = "users"

CREATE_TABLE_ITEMS = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_ITEMS} (
        id    INTEGER PRIMARY KEY,
        name  TEXT NOT NULL,
        price REAL NOT NULL
    );
"""

CREATE_TABLE_USERS = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
        id       INTEGER PRIMARY KEY,
        username TEXT    UNIQUE NOT NULL,
        password TEXT    NOT NULL
);
"""
