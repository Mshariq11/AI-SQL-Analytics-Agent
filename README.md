# Supermarket SQL Query Agent

> **Natural Language → SQL → Validation → SQLite → Results**

A lightweight AI-powered data application that lets users ask questions
about supermarket sales in natural language. The system generates SQLite
SQL using database schema context, validates the SQL as read-only,
executes it against a local SQLite database, and displays the results
through a Streamlit interface.

---

## Project Snapshot

  Area               Details

---

  Dataset            Supermarket Sales CSV
  Source records     1,000
  Unique invoices    1,000
  Database           SQLite
  Main table         `sales`
  Columns            18
  Interface          Streamlit
  LLM                OpenAI API
  Query policy       Read-only `SELECT` / `WITH`
  Primary language   Python

---

## What It Does

- Accepts a natural-language business question.
- Reads the database schema dynamically.
- Builds a schema-aware SQL generation prompt.
- Uses an LLM to generate SQLite-compatible SQL.
- Validates generated SQL before execution.
- Blocks database-modifying statements.
- Executes approved queries against SQLite.
- Displays generated SQL and query results.
- Provides database context and lightweight query history in the UI.
- Handles application/API errors without exposing unnecessary
  technical details.

---

## Project Flow

```text
User Question
     ↓
Streamlit Application
     ↓
SQLAgent
     ↓
Database Schema Context
     ↓
LLM / SQL Generation
     ↓
SQL Validation
     ↓
Read-only SQL
     ↓
SQLite Database
     ↓
Query Results
     ↓
Streamlit Display
```

---

## Architecture

```text
┌──────────────────────┐
│   Streamlit UI       │
│  User Question       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      SQLAgent        │
│  Orchestration       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Schema + SQL Prompt  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│        LLM           │
│   SQL Generation     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   SQL Validation     │
│ SELECT / WITH only   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ SQLite Query Layer   │
└──────────┬───────────┘
           ↓
      sales table
           ↓
        Results
```

---

## Repository Structure

```text
supermarket-sql-agent/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py          # SQLAgent orchestration
│   ├── prompts.py        # SQL generation prompt
│   ├── tools.py          # Database/schema tools
│   └── validation.py     # SQL safety validation
│
├── database/
│   ├── __init__.py
│   ├── connection.py     # SQLite connection
│   ├── query.py          # Read-only query execution
│   ├── schema.py         # Table/schema discovery
│   └── setup.py          # CSV → SQLite pipeline
│
├── scripts/
│   ├── __init__.py
│   └── setup_database.py # Database setup entry point
│
├── data/
│   └── supermarket_sales.csv
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Database

The project converts the source CSV into a local SQLite database.

### `sales` table

The table contains 18 fields covering:

- Invoice information
- Branch and city
- Customer type
- Gender
- Product line
- Unit price and quantity
- Tax and total sales
- Date and time
- Payment method
- COGS
- Gross margin
- Gross income
- Rating
- Rating category

### Database setup

```bash
python -m scripts.setup_database
```

The setup process:

1. Loads the CSV.
2. Validates expected columns.
3. Performs data-quality checks.
4. Transforms date/time fields.
5. Creates the SQLite database.
6. Loads the `sales` table.
7. Validates row counts and unique invoices.

---

## SQL Safety

The application is intentionally **read-only**.

Allowed:

```sql
SELECT ...
```

```sql
WITH ...
SELECT ...
```

Blocked operations include:

- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`
- `CREATE`
- `REPLACE`
- Multiple SQL statements
- SQL comments

SQL is validated before it reaches the database execution layer.

```text
Generated SQL
     ↓
Validation
     ↓
Allowed? ── No → Reject
     │
    Yes
     ↓
SQLite
```

---

## Example Questions

The agent can handle questions such as:

- What is the total sales for each branch?
- Which product line has the highest sales?
- What is the average rating by branch?
- How many transactions used each payment method?

Example generated query:

```sql
SELECT
    branch,
    ROUND(SUM(total), 2) AS total_sales
FROM sales
GROUP BY branch
ORDER BY total_sales DESC;
```

Example validated result:

```text
C    110569.0
A    106202.0
B    106199.0
```

---

## Technology Stack

- **Python** --- application and data-processing logic
- **Pandas** --- CSV/data preparation
- **SQLite** --- local analytical database
- **OpenAI API** --- natural-language-to-SQL generation
- **Streamlit** --- interactive application interface
- **python-dotenv** --- environment configuration
- **Git/GitHub** --- version control and portfolio delivery

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd supermarket-sql-agent
```

### 2. Create and activate an environment

Using Conda:

```bash
conda create -n supermarket-sql-agent python=3.11
conda activate supermarket-sql-agent
```

Or use another Python virtual environment.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create `.env` from `.env.example`:

```text
LLM_API_KEY=your_api_key_here
```

Never commit the real `.env` file or API key.

### 5. Build the database

```bash
python -m scripts.setup_database
```

### 6. Run the application

```bash
streamlit run app.py
```

---

## Engineering Decisions

### Separate database layer

Database connection, schema discovery, setup, and query execution are
separated from the agent logic.

### Separate validation layer

Generated SQL is validated independently before execution. This creates
a clear safety boundary between the LLM and the database.

### Schema-aware prompting

The LLM receives the actual database schema rather than relying on
assumed table or column names.

### SQLite

SQLite keeps the project lightweight, reproducible, and easy to run
locally while still demonstrating practical SQL-agent architecture.

### Streamlit

Streamlit provides a simple interface for demonstrating the complete
natural-language-to-SQL workflow without introducing unnecessary
frontend complexity.

---

## Validation Performed

The project was validated through the following checks:

- Database successfully recreated from the CSV.
- `sales` table created successfully.
- 1,000 rows loaded.
- 1,000 unique invoices confirmed.
- 18 database columns confirmed.
- SQLite connection verified.
- Normal `SELECT` queries verified.
- `WITH` queries verified.
- Destructive SQL rejected.
- Database row count rechecked after safety tests.
- SQLAgent import and orchestration verified.
- Streamlit application behavior verified.

---

## Current Limitations

- Uses a single local SQLite database.
- Current dataset is centered on one `sales` table.
- Requires access to an LLM API for natural-language SQL generation.
- No user authentication.
- Query history is application/session-level rather than a persistent
  analytics system.
- Designed as a portfolio/learning application rather than a
  production enterprise platform.

---

## Future Improvements

Possible extensions include:

- Multi-table database support.
- More advanced SQL parsing and validation.
- Query-result visualizations.
- Persistent query history.
- Authentication and access control.
- Production database support.
- Automated SQL-generation evaluation.
- Monitoring and observability.

These are intentionally outside the current scope.

---

## Project Goal

The main goal is to demonstrate how an AI-assisted SQL application can
combine:

**Natural Language + LLMs + SQL + Data Validation + SQLite + Streamlit**

into a small, understandable, and safety-conscious data application.

---

## Status

**Core project complete.**

The application, database pipeline, SQL-agent layer, validation layer,
and Streamlit interface have been implemented and validated.
