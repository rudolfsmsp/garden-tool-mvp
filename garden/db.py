import sqlite3


def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema(db_path):
    with connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS beds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                location_hint TEXT,
                photo_path TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bed_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (bed_id) REFERENCES beds(id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bed_id INTEGER NOT NULL,
                task_type TEXT NOT NULL,
                task_date TEXT,
                completed_at TEXT,
                photo_path TEXT,
                FOREIGN KEY (bed_id) REFERENCES beds(id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("reminders_enabled", "1"),
        )


def fetch_all(db_path, query, params=()):
    with connect(db_path) as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()


def fetch_one(db_path, query, params=()):
    with connect(db_path) as conn:
        cur = conn.execute(query, params)
        return cur.fetchone()


def execute(db_path, query, params=()):
    with connect(db_path) as conn:
        conn.execute(query, params)
        conn.commit()
