
import sqlite3
from contextlib import contextmanager

from app.auth.config import DATABASE_PATH


def initialize_database():
    """Crea la tabla de usuarios si todavía no existe."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@contextmanager
def get_db_connection():
    """Proporciona una conexión SQLite y la cierra al terminar."""
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
