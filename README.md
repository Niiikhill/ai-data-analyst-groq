# 🤖 AI Data Analyst 2.0 (Groq Edition)

AI Data Analyst 2.0 is an **LLM-powered natural language to SQL analytics assistant** that allows users to ask questions about structured data in plain English and get instant insights.

This project uses **Streamlit** for the frontend, **SQLite** as the database, **LangChain** for prompt orchestration, and **Groq LLM API** to convert user questions into executable SQL queries.

---

## ✨ Features

- 🔍 Ask questions about your database in **natural language**
- 🧠 Automatically extracts database schema from SQLite
- 📝 Converts user questions into **valid SQL queries**
- ⚡ Executes generated SQL on the database in real time
- 📊 Displays both:
  - Generated SQL query
  - Query results
- 🔐 Secure API key handling using `.env`
- 🚀 Uses **Groq API** for fast inference (no local Ollama setup needed)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **SQLite**
- **SQLAlchemy**
- **LangChain**
- **Groq API**
- **python-dotenv**

---

## 📂 Project Structure

```bash
ai-data-analyst-groq/
├── main.py               # Schema extraction + text-to-SQL + DB query execution
├── frontend.py           # Streamlit UI
├── create_database.py    # Creates sample SQLite database with dummy data
├── amazon.db             # Sample SQLite database
├── .env.example          # Example environment variables file
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
