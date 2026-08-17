from pathlib import Path
import sqlite3

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "supermarket_sales.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "supermarket.db"


# Expected source columns
EXPECTED_COLUMNS = [
    "Invoice ID",
    "Branch",
    "City",
    "Customer type",
    "Gender",
    "Product line",
    "Unit price",
    "Quantity",
    "Tax 5%",
    "Total",
    "Date",
    "Time",
    "Payment",
    "cogs",
    "gross margin percentage",
    "gross income",
    "Rating",
    "New Rating",
]


# Source → database column mapping
COLUMN_MAPPING = {
    "Invoice ID": "invoice_id",
    "Branch": "branch",
    "City": "city",
    "Customer type": "customer_type",
    "Gender": "gender",
    "Product line": "product_line",
    "Unit price": "unit_price",
    "Quantity": "quantity",
    "Tax 5%": "tax_5_percent",
    "Total": "total",
    "Date": "date",
    "Time": "time",
    "Payment": "payment",
    "cogs": "cogs",
    "gross margin percentage": "gross_margin_percentage",
    "gross income": "gross_income",
    "Rating": "rating",
    "New Rating": "new_rating",
}


def load_source_data() -> pd.DataFrame:
    """Load the supermarket CSV file."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Source dataset not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    if df.empty:
        raise ValueError("Source dataset is empty.")

    return df


def validate_source_columns(df: pd.DataFrame) -> None:
    """Validate that all required source columns are present."""

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def validate_data_quality(df: pd.DataFrame) -> None:
    """Validate basic source-data quality."""

    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    if missing_values > 0:
        raise ValueError(
            f"Dataset contains {missing_values} missing values."
        )

    if duplicate_rows > 0:
        raise ValueError(
            f"Dataset contains {duplicate_rows} duplicate rows."
        )


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform source data into the database schema."""

    df = df.copy()

    # Rename columns to SQL-friendly names
    df = df.rename(columns=COLUMN_MAPPING)

    # Normalize date
    df["date"] = pd.to_datetime(
        df["date"],
        format="%m/%d/%Y",
    ).dt.strftime("%Y-%m-%d")

    # Normalize time
    df["time"] = pd.to_datetime(
        df["time"],
        format="%H:%M",
    ).dt.strftime("%H:%M:%S")

    return df


def create_database(df: pd.DataFrame) -> None:
    """Create the SQLite database and load the sales table."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    with sqlite3.connect(DATABASE_PATH) as connection:

        connection.execute(
            """
            CREATE TABLE sales (
                invoice_id TEXT PRIMARY KEY,
                branch TEXT,
                city TEXT,
                customer_type TEXT,
                gender TEXT,
                product_line TEXT,
                unit_price REAL,
                quantity INTEGER,
                tax_5_percent REAL,
                total REAL,
                date TEXT,
                time TEXT,
                payment TEXT,
                cogs REAL,
                gross_margin_percentage REAL,
                gross_income REAL,
                rating INTEGER,
                new_rating TEXT
            );
            """
        )

        df.to_sql(
            "sales",
            connection,
            if_exists="append",
            index=False,
        )


def verify_database() -> None:
    """Verify that the SQLite database was created correctly."""

    with sqlite3.connect(DATABASE_PATH) as connection:

        row_count = connection.execute(
            "SELECT COUNT(*) FROM sales;"
        ).fetchone()[0]

        unique_invoice_count = connection.execute(
            "SELECT COUNT(DISTINCT invoice_id) FROM sales;"
        ).fetchone()[0]

    if row_count == 0:
        raise ValueError("Database contains no records.")

    if row_count != unique_invoice_count:
        raise ValueError(
            "Invoice ID uniqueness validation failed."
        )

    print(f"Database created: {DATABASE_PATH}")
    print(f"Rows loaded: {row_count}")
    print(f"Unique invoices: {unique_invoice_count}")


def setup_database() -> None:
    """Run the complete CSV-to-SQLite pipeline."""

    print("Starting database setup...")

    df = load_source_data()

    print(f"Source rows: {len(df)}")

    validate_source_columns(df)
    print("Column validation passed.")

    validate_data_quality(df)
    print("Data quality validation passed.")

    df = transform_data(df)
    print("Data transformation completed.")

    create_database(df)
    print("SQLite database created.")

    verify_database()
    print("Database validation passed.")

    print("Database setup completed successfully.")


if __name__ == "__main__":
    setup_database()