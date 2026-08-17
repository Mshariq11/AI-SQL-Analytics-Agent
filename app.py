import streamlit as st
import sqlite3

def check_database_connection(db_path):
    try:
        connection = sqlite3.connect(db_path)
        connection.execute("SELECT 1")
        connection.close()
        return True
    except Exception:
        return False

from agent.agent import SQLAgent
st.set_page_config(
    page_title="Supermarket SQL Agent",
    page_icon="🧠",
    layout="wide",
)


st.title("Supermarket SQL Agent")

st.write(
    "Ask questions about the supermarket sales database "
    "using natural language."
)


if "response" not in st.session_state:
    st.session_state.response = None

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "processing" not in st.session_state:
    st.session_state.processing = False

question = st.text_input(
    "Ask a question about the sales data",
    placeholder="e.g. What is the total sales for each branch?",
    max_chars=500,
)

st.caption(
    f"{len(question)} / 500 characters"
)

st.caption(
    "Use natural language to ask questions about the supermarket sales data."
)

if st.button(
    "Processing..." if st.session_state.processing else "Ask",
    type="primary",
    disabled=st.session_state.processing,
):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.processing = True

        try:
            with st.spinner("Processing your question..."):
                agent = SQLAgent()
                response = agent.ask(question)

                st.session_state.query_history = (
                    st.session_state.query_history[-10:]
                )

        except ValueError as exc:
            st.warning(str(exc))

        except Exception:
            st.error(
                "The SQL agent could not process your request. "
                "Please try again later."
            )

        finally:
            st.session_state.processing = False

if st.button("New Question"):
    st.session_state.response = None
    st.rerun()

if st.session_state.response:
    response = st.session_state.response

    st.subheader("Question")
    st.write(response["question"])

    with st.expander("Generated SQL", expanded=False):
        st.code(response["sql"], language="sql")

    st.subheader("Results")
    results = response["results"]

    if results:
        columns = list(results[0].keys())
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Result Rows",
                value=len(results),
                )
            with col2:
                st.metric(
                    label="Columns",
                    value=len(columns),
                    )
                st.caption(
                    "Returned columns: " + ", ".join(columns)
                    )
                st.dataframe(
                    results,
                    use_container_width=True,
                    )
    else:
        st.info(
            "Ask a question about the supermarket sales data "
            "to get started."
            )
        st.markdown("### Example questions")
        st.markdown(
            """
            - What is the total sales for each branch?
            - What are the top 5 product lines by sales?
            - What is the average rating by branch?
            """)

from database.schema import get_table_schema, get_tables

with st.sidebar:
    database_connected = check_database_connection("data/supermarket.db")
    st.header("Database")
    if database_connected:
        st.success("Connected")
    else:
        st.error("Unavailable")

    tables = get_tables()

    st.write("**Engine:** SQLite")
    st.write("**Tables:**")

    for table in tables:
        st.write(f"- `{table}`")

    if "sales" in tables:
        columns = get_table_schema("sales")
        st.write(f"**Columns:** {len(columns)}")

with st.sidebar:
    st.subheader("Query History")

    if st.session_state.query_history:
        for index, item in enumerate(
            reversed(st.session_state.query_history),
            start=1,
        ):
            st.caption(f"{index}. {item}")

        if st.button("Clear History"):
            st.session_state.query_history = []
            st.rerun()

    else:
        st.caption("No questions asked yet.")

    st.divider()
    with st.expander("About this agent"):
        st.write(
        "This application converts natural-language questions "
        "into read-only SQLite SQL queries and executes them "
        "against the supermarket sales database."
        )
        st.write("**Pipeline:**")
        st.write(
        "Question → SQL Generation → SQL Validation → "
        "SQLite Execution → Results"
        )

    st.divider()
    with st.expander("Example questions"):
        st.write("Try questions like:")
        st.caption("• What is the total sales for each branch?")
        st.caption("• Which product line has the highest sales?")
        st.caption("• What is the average rating by branch?")
        st.caption("• How many transactions used each payment method?")

st.divider()

st.caption(
    "Supermarket SQL Agent • Natural Language → SQLite SQL → Results"
)