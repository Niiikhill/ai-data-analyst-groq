# Step1: Extract Schema
from sqlalchemy import create_engine, inspect
import json
import re
import sqlite3
import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

db_url = "sqlite:///amazon.db"


def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col["name"] for col in columns]

    return json.dumps(schema, indent=2)


def text_to_sql(schema, prompt):
    SYSTEM_PROMPT = """
    You are an expert SQL generator.

    Given a database schema and a user prompt, generate a valid SQLite SQL query that answers the prompt.

    Rules:
    - Only use the tables and columns provided in the schema.
    - Generate only valid SQLite-compatible SQL.
    - Output ONLY the SQL query.
    - Do NOT add explanations.
    - Do NOT add markdown code fences.
    - Do NOT add preamble like "Here is your SQL query".
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Schema:\n{schema}\n\nQuestion: {user_prompt}\n\nSQL Query:")
    ])

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Please add it to your .env file.")

    model = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    chain = prompt_template | model

    raw_response = chain.invoke({
        "schema": schema,
        "user_prompt": prompt
    })

    sql_query = raw_response.content.strip()
    sql_query = re.sub(r"```sql|```", "", sql_query, flags=re.IGNORECASE).strip()

    return sql_query


def get_data_from_database(prompt):
    schema = extract_schema(db_url)
    sql_query = text_to_sql(schema, prompt)

    conn = sqlite3.connect("amazon.db")
    cursor = conn.cursor()

    try:
        res = cursor.execute(sql_query)
        results = res.fetchall()
    except Exception as e:
        conn.close()
        return f"Error executing SQL: {e}\nGenerated SQL: {sql_query}"

    conn.close()
    return results