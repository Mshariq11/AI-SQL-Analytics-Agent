from database.connection import get_connection


def execute_query(query: str) -> list[dict]:
    """Execute a read-only SQL query and return the results."""

    query = query.strip()

    if not query:
        raise ValueError("SQL query cannot be empty.")

    normalized_query = query.strip().lower()
    if not (
        normalized_query.startswith("select")
        or normalized_query.startswith("with")
        ):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
            )

    with get_connection() as connection:
        cursor = connection.execute(query)

        columns = [
            column[0]
            for column in cursor.description
        ]

        rows = cursor.fetchall()

    return [
        dict(zip(columns, row))
        for row in rows
    ]