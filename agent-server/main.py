from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import sqlite3
import os
import asyncio # Added for Playwright
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.llms import OpenAI # Placeholder, actual model will be configured
from .agent.core import create_ai_tools_agent # Import the agent factory

app = FastAPI()

DATABASE_FILE = "ai_tools.db"

# Initialize the agent globally
agent_executor = create_ai_tools_agent()

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
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
    description: str = None
    url: str = None
    source: str = None
    search_query: str = None

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Top AI Tools Agent API"}

@app.get("/tools", response_model=List[ToolItem])
async def get_ai_tools():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, url, source, search_query FROM ai_tools ORDER BY timestamp DESC")
    tools = cursor.fetchall()
    conn.close()
    return [ToolItem(name=t[0], description=t[1], url=t[2], source=t[3], search_query=t[4]) for t in tools]

@app.post("/tools")
async def add_ai_tool(tool_item: ToolItem):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ai_tools (name, description, url, source, search_query) VALUES (?, ?, ?, ?, ?)",
        (tool_item.name, tool_item.description, tool_item.url, tool_item.source, tool_item.search_query)
    )
    conn.commit()
    conn.close()
    return {"message": "Tool added successfully", "tool": tool_item}

@app.post("/run_agent")
async def run_agent_task(task: str):
    result = await agent_executor.ainvoke({"input": task})
    return {"result": result}
