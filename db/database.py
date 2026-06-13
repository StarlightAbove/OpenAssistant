import sqlite3
from pathlib import Path
from db.models import (
    CREATE_SNAPSHOTS_TABLE,
    CREATE_BRIEFINGS_TABLE,
    CREATE_SNAPSHOTS_INDEX,
)

DB_PATH = Path(__file__).parent.parent / "data" / "openassistant.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    conn.execute("PRAGMA journal_mode=WAL")  # safer for concurrent access
    return conn


def initialize():
    """Create tables and indexes if they don't exist. Safe to call on every run."""
    with get_connection() as conn:
        conn.execute(CREATE_SNAPSHOTS_TABLE)
        conn.execute(CREATE_BRIEFINGS_TABLE)
        conn.execute(CREATE_SNAPSHOTS_INDEX)
        conn.commit()