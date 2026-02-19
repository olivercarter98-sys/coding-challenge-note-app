import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "entries.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                email     TEXT    NOT NULL,
                notes     TEXT,
                created_at TEXT   NOT NULL
            )
        """)
        conn.commit()


def insert_entry(name: str, email: str, notes: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO entries (name, email, notes, created_at) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), notes.strip(), datetime.utcnow().isoformat(sep=" ", timespec="seconds"))
        )
        conn.commit()
        return cursor.lastrowid


def get_all_entries() -> list:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM entries ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def update_entry(entry_id: int, name: str, email: str, notes: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE entries SET name = ?, email = ?, notes = ? WHERE id = ?",
            (name.strip(), email.strip().lower(), notes.strip(), entry_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_entry(entry_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        conn.commit()
        return cursor.rowcount > 0