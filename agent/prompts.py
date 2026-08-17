def build_sql_prompt(
    user_question: str,
    schema: str,
) -> str:
    """Build the prompt used to generate SQLite SQL."""

    if not user_question.strip():
        raise ValueError("User question cannot be empty.")

    if not schema.strip():
        raise ValueError("Database schema cannot be empty.")

    return f"""
You are a SQL analyst working with a SQLite database.

Your task is to convert the user's natural-language question
into a valid SQLite SQL query.

DATABASE SCHEMA:
{schema}

RULES:
1. Use only tables and columns provided in the schema.
2. Generate SQLite-compatible SQL.
3. Answer the user's question directly.
4. Do not invent tables, columns, metrics, or data.
5. Use appropriate aggregation, filtering, grouping, and ordering.
6. Return only a SELECT statement.
7. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   REPLACE, or other database-modifying statements.
8. Do not include Markdown code fences.
9. Do not include explanations or commentary.
10. If the question cannot be answered using the provided schema,
    do not invent an answer.

USER QUESTION:
{user_question}

Return only the SQL query.
""".strip()