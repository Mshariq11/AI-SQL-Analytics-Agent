from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "supermarket.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a connection to the SQLite database."""

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    return connection

from database.connection import get_connection

connection = get_connection()