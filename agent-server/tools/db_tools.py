import sqlite3
from langchain_core.tools import tool
from ..main import DATABASE_FILE # Import DATABASE_FILE from main.py

@tool
def store_ai_tool_in_db(name: str, description: str = None, url: str = None, source: str = None, search_query: str = None) -> str:
    """Stores an AI tool's information into the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ai_tools (name, description, url, source, search_query) VALUES (?, ?, ?, ?, ?)",
            (name, description, url, source, search_query)
        )
        conn.commit()
        return f"Successfully stored AI tool: {name}"
    except Exception as e:
        conn.rollback()
        return f"Error storing AI tool: {e}"
    finally:
        conn.close()
