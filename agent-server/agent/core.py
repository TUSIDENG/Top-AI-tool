from langchain.agents import create_agent
from tools.search_tools import google_search, bing_search, baidu_search
from tools.db_tools import store_ai_tool_in_db
from config import config

def create_ai_tools_agent():
    tools = [bing_search, baidu_search, store_ai_tool_in_db]
    
    system_prompt = "You are an AI assistant that helps find and categorize top AI tools. " \
                   "Use the available search tools to find information and the store_ai_tool_in_db tool to save relevant findings. " \
                   "When you have found sufficient information, provide a summary and stop searching."

    agent = create_agent(
        model=config.AGENT_MODEL,
        tools=tools,
        system_prompt=system_prompt
    )
    return agent
