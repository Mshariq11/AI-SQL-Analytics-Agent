from database.query import execute_query
from database.schema import get_tables, get_table_schema


def get_database_tables() -> list[str]:
    """Return the available database tables."""

    return get_tables()


def get_database_schema(table_name: str) -> list[dict]:
    """Return the schema for a specific database table."""

    if not table_name.strip():
        raise ValueError(
            "Table name cannot be empty."
        )

    return get_table_schema(table_name)


def run_sql_query(query: str) -> list[dict]:
    """Execute a read-only SQL query."""

    return execute_query(query)