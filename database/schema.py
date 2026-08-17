from database.connection import get_connection


def get_tables() -> list[str]:
    """Return all user-defined tables in the database."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
            """
        ).fetchall()

    return [row[0] for row in rows]


def get_table_schema(table_name: str) -> list[dict]:
    """Return column information for a table."""

    with get_connection() as connection:
        rows = connection.execute(
            f"PRAGMA table_info({table_name});"
        ).fetchall()

    return [
        {
            "name": row[1],
            "type": row[2],
            "not_null": bool(row[3]),
            "default": row[4],
            "primary_key": bool(row[5]),
        }
        for row in rows
    ]