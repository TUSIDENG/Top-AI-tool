import sqlite3
from langchain_core.tools import tool
from config import config

@tool
def store_ai_tool_in_db(
    name: str, 
    description: str = None, 
    url: str = None, 
    source: str = None, 
    search_query: str = None
) -> str:
    """Stores an AI tool's information into the SQLite database."""
    
    print(f"🔧 TOOL_RUNTIME: Starting to store AI tool: {name}")
    
    conn = sqlite3.connect(config.get_database_path())
    cursor = conn.cursor()
    try:
        print("🔧 TOOL_RUNTIME: Connecting to database...")
        
        cursor.execute(
            "INSERT INTO ai_tools (name, description, url, source, search_query) VALUES (?, ?, ?, ?, ?)",
            (name, description, url, source, search_query)
        )
        conn.commit()
        
        print(f"✅ TOOL_RUNTIME: Successfully stored AI tool: {name}")
        
        return f"Successfully stored AI tool: {name}"
    except Exception as e:
        conn.rollback()
        error_msg = f"Error storing AI tool: {e}"
        
        print(f"❌ TOOL_RUNTIME: Error: {error_msg}")
        
        return error_msg
    finally:
        conn.close()
