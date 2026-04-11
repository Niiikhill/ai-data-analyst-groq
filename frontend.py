# Step3: Build Streamlit frontend
import streamlit as st
from main import get_data_from_database, text_to_sql, extract_schema, db_url

st.set_page_config(
    page_title="AI Data Analyst 2.0",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Data Analyst 2.0")
st.markdown("Ask questions about your data in natural language and get instant SQL-based insights.")

user_query = st.text_area(
    "💬 Enter your question:",
    placeholder="e.g., Show total sales by customer"
)

if st.button("Analyze"):
    if user_query.strip() == "":
        st.warning("Please enter a question to analyze.")
    else:
        with st.spinner("Analyzing your query..."):
            try:
                # Extract schema
                schema = extract_schema(db_url)

                # Generate SQL query
                sql_query = text_to_sql(schema, user_query)

                # Run SQL query
                database_response = get_data_from_database(user_query)

                st.success("Analysis complete!")

                # Show generated SQL
                st.subheader("🧠 Generated SQL Query")
                st.code(sql_query, language="sql")

                # Show results
                st.subheader("📊 Query Results")

                if isinstance(database_response, str) and database_response.startswith("Error"):
                    st.error(database_response)
                elif len(database_response) == 0:
                    st.info("No results found.")
                else:
                    st.write(database_response)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("""
    <style>
    textarea {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)