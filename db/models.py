CREATE_SNAPSHOTS_TABLE = """
CREATE TABLE IF NOT EXISTS daily_snapshots (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT NOT NULL,           -- YYYY-MM-DD
    source      TEXT NOT NULL,           -- e.g. 'gmail', 'todoist'
    data        TEXT NOT NULL,           -- JSON blob
    captured_at TEXT NOT NULL            -- full ISO timestamp
);
"""

CREATE_BRIEFINGS_TABLE = """
CREATE TABLE IF NOT EXISTS briefings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date         TEXT NOT NULL,          -- YYYY-MM-DD
    content      TEXT NOT NULL,          -- full briefing text
    generated_at TEXT NOT NULL
);
"""

CREATE_SNAPSHOTS_INDEX = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_snapshots_date_source
ON daily_snapshots (date, source);
"""