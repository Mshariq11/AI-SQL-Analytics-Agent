import re


FORBIDDEN_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "replace",
    "truncate",
    "attach",
    "detach",
    "pragma",
}


def validate_sql(sql: str) -> str:
    """Validate that SQL is a read-only SELECT statement."""

    if not sql or not sql.strip():
        raise ValueError("SQL query cannot be empty.")

    cleaned_sql = sql.strip()

    # Remove one trailing semicolon for validation.
    normalized_sql = cleaned_sql.rstrip(";").strip()

    if not normalized_sql:
        raise ValueError("SQL query cannot be empty.")

    # Only SELECT or WITH queries are allowed.
    if not re.match(
        r"^(SELECT|WITH)\b",
        normalized_sql,
        re.IGNORECASE,
    ):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
        )

    # Reject SQL comments.
    if "--" in normalized_sql or "/*" in normalized_sql:
        raise ValueError(
            "SQL comments are not allowed."
        )

    # Reject multiple SQL statements.
    if ";" in normalized_sql:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    # Check for forbidden SQL keywords.
    words = set(
        re.findall(
            r"\b[a-zA-Z_]+\b",
            normalized_sql.lower(),
        )
    )

    forbidden_found = words.intersection(FORBIDDEN_KEYWORDS)

    if forbidden_found:
        raise ValueError(
            "Forbidden SQL operation detected: "
            f"{sorted(forbidden_found)}"
        )

    return normalized_sql