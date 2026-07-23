import sqlite3
from pathlib import Path
from typing import List, Optional

DB_PATH = Path("data/school_check.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create the SQLite schema required by the application."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        conn = _connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                university TEXT,
                country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS saved_universities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                country TEXT,
                domain TEXT,
                website TEXT,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()
    except sqlite3.Error as exc:
        raise RuntimeError(f"Failed to initialize database: {exc}") from exc
    finally:
        conn.close()


def save_search(university: str, country: str) -> bool:
    """Store a university search for history tracking."""
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO searches (university, country) VALUES (?, ?)",
            ((university or "").strip(), (country or "").strip()),
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def get_total_searches() -> int:
    """Return the total number of recorded searches."""
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM searches")
        return int(cursor.fetchone()[0])
    except sqlite3.Error:
        return 0
    finally:
        conn.close()


def get_saved_university_count() -> int:
    """Return the number of saved universities."""
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM saved_universities")
        return int(cursor.fetchone()[0])
    except sqlite3.Error:
        return 0
    finally:
        conn.close()


def save_university(name: str, country: str, domain: str, website: str) -> bool:
    """Persist a university if it is not already saved."""
    normalized_name = (name or "").strip()
    if not normalized_name:
        return False

    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM saved_universities WHERE LOWER(TRIM(name)) = LOWER(?) LIMIT 1",
            (normalized_name,),
        )
        if cursor.fetchone():
            return False

        cursor.execute(
            """
            INSERT INTO saved_universities (name, country, domain, website)
            VALUES (?, ?, ?, ?)
            """,
            (
                normalized_name,
                (country or "").strip(),
                (domain or "").strip(),
                (website or "").strip(),
            ),
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def get_saved_universities() -> List[tuple]:
    """Return all saved universities sorted by the most recent save."""
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name, country, domain, website, saved_at
            FROM saved_universities
            ORDER BY saved_at DESC
            """
        )
        return cursor.fetchall()
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def delete_university(name: str) -> bool:
    """Delete a saved university by name."""
    normalized_name = (name or "").strip()
    if not normalized_name:
        return False

    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM saved_universities WHERE LOWER(TRIM(name)) = LOWER(?)",
            (normalized_name,),
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def get_search_history(limit: int = 10) -> List[dict]:
    """Return recent searches in reverse-chronological order."""
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT university, country, created_at
            FROM searches
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


initialize_database()
