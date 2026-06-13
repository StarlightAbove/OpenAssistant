import json
from datetime import date, timedelta
from db.database import get_connection


def save_snapshot(source: str, data: dict, run_date: date = None):
    run_date = run_date or date.today()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO daily_snapshots (date, source, data, captured_at)
            VALUES (?, ?, ?, datetime('now'))
            ON CONFLICT(date, source) DO UPDATE SET
                data = excluded.data,
                captured_at = excluded.captured_at
            """,
            (run_date.isoformat(), source, json.dumps(data)),
        )
        conn.commit()


def get_snapshot(source: str, run_date: date = None) -> dict | None:
    run_date = run_date or date.today()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT data FROM daily_snapshots WHERE date = ? AND source = ?",
            (run_date.isoformat(), source),
        ).fetchone()
    return json.loads(row["data"]) if row else None


def get_yesterday_snapshot(source: str) -> dict | None:
    yesterday = date.today() - timedelta(days=1)
    return get_snapshot(source, run_date=yesterday)


def save_briefing(content: str):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO briefings (date, content, generated_at)
            VALUES (?, ?, datetime('now'))
            """,
            (date.today().isoformat(), content),
        )
        conn.commit()


def get_recent_briefings(n: int = 7) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT date, content FROM briefings ORDER BY date DESC LIMIT ?",
            (n,),
        ).fetchall()
    return [dict(row) for row in rows]