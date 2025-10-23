from langchain.agents import create_agent
from tools.search_tools import google_search, bing_search, baidu_search
from tools.db_tools import store_ai_tool_in_db
from config import config

def create_ai_tools_agent():
    tools = [bing_search, baidu_search, store_ai_tool_in_db]
    
    system_prompt = """You are an AI assistant specialized in finding and categorizing top AI tools. 

Guidelines:
1. Use search tools to find information about AI tools
2. Each search should focus on specific categories or use cases (e.g., "AI image generation tools", "machine learning frameworks", "AI coding assistants")
3. Limit each search to gather approximately 50 relevant results - avoid excessive searching
4. Use the store_ai_tool_in_db tool to save high-quality, relevant findings
5. Focus on tools that are actively maintained, have good documentation, and serve practical use cases
6. After gathering sufficient information, provide a comprehensive summary of the findings
7. Stop searching once you have collected enough diverse and high-quality tools

Remember: Quality over quantity. It's better to have 50 well-researched tools than hundreds of low-quality ones."""
    
    agent = create_agent(
        model=config.AGENT_MODEL,
        tools=tools,
        system_prompt=system_prompt
    )
    return agent
