from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import asyncio
from agent.core import create_ai_tools_agent
from config import config

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent globally
agent_executor = create_ai_tools_agent()

def init_db():
    conn = sqlite3.connect(config.get_database_path())
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            url TEXT,
            source TEXT,
            search_query TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database on startup
init_db()

class ToolItem(BaseModel):
    name: str
    description: str = ""
    url: str = ""
    source: str = ""
    search_query: str = ""

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Top AI Tools Agent API"}

@app.get("/tools", response_model=List[ToolItem])
async def get_ai_tools(
    limit: int = Query(50, ge=1, le=100, description="Number of tools to return"),
    offset: int = Query(0, ge=0, description="Number of tools to skip"),
    search: Optional[str] = Query(None, description="Search term to filter tools by name or description")
):
    conn = sqlite3.connect(config.get_database_path())
    cursor = conn.cursor()
    
    if search:
        query = """
            SELECT name, description, url, source, search_query 
            FROM ai_tools 
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """
        search_pattern = f"%{search}%"
        cursor.execute(query, (search_pattern, search_pattern, limit, offset))
    else:
        query = """
            SELECT name, description, url, source, search_query 
            FROM ai_tools 
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (limit, offset))
    
    tools = cursor.fetchall()
    conn.close()
    
    # Convert None values to empty strings for Pydantic compatibility
    processed_tools = []
    for t in tools:
        processed_tools.append(ToolItem(
            name=t[0] or "",
            description=t[1] or "",
            url=t[2] or "",
            source=t[3] or "",
            search_query=t[4] or ""
        ))
    
    return processed_tools

@app.post("/tools")
async def add_ai_tool(tool_item: ToolItem):
    conn = sqlite3.connect(config.get_database_path())
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ai_tools (name, description, url, source, search_query) VALUES (?, ?, ?, ?, ?)",
        (tool_item.name, tool_item.description, tool_item.url, tool_item.source, tool_item.search_query)
    )
    conn.commit()
    conn.close()
    return {"message": "Tool added successfully", "tool": tool_item}

class AgentTask(BaseModel):
    task: str

@app.post("/run_agent")
async def run_agent_task(agent_task: AgentTask):
    print(f"🔧 TOOL_RUNTIME: Starting agent task: {agent_task.task}")
    result = await agent_executor.ainvoke({"input": agent_task.task}, config={"recursion_limit": 100})
    print(f"✅ TOOL_RUNTIME: Agent task completed")
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
