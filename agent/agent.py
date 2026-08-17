import os

from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import build_sql_prompt
from agent.tools import get_database_schema, run_sql_query
from agent.validation import validate_sql


load_dotenv()


class SQLAgent:
    """Generate and execute read-only SQL queries."""

    def __init__(self, model: str = "gpt-5-mini"):
        self.model = model

        api_key = os.getenv("LLM_API_KEY")

        if not api_key:
            raise ValueError(
                "LLM_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

    def _get_schema_text(self) -> str:
        """Build a readable schema description for the LLM."""

        columns = get_database_schema("sales")

        schema_lines = ["TABLE sales ("]

        for column in columns:
            primary_key = (
                " PRIMARY KEY"
                if column["primary_key"]
                else ""
            )

            schema_lines.append(
                f"    {column['name']} "
                f"{column['type']}{primary_key},"
            )

        schema_lines[-1] = schema_lines[-1].rstrip(",")
        schema_lines.append(")")

        return "\n".join(schema_lines)

    def generate_sql(self, user_question: str) -> str:
        """Generate SQL from a natural-language question."""

        if not user_question.strip():
            raise ValueError(
                "User question cannot be empty."
            )

        schema = self._get_schema_text()

        prompt = build_sql_prompt(
            user_question=user_question,
            schema=schema,
        )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text.strip()

    def execute_sql(self, sql: str) -> list[dict]:
        """Validate and execute a read-only SQL query."""

        validated_sql = validate_sql(sql)

        return run_sql_query(validated_sql)

    def ask(self, user_question: str) -> dict:
        """Process a natural-language question end to end."""

        if not user_question.strip():
            raise ValueError(
                "User question cannot be empty."
            )

        sql = self.generate_sql(user_question)

        results = self.execute_sql(sql)

        return {
            "question": user_question,
            "sql": sql,
            "results": results,
        }