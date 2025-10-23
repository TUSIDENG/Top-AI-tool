from langchain.agents import create_agent
from tools.search_tools import google_search, bing_search, baidu_search
from tools.db_tools import store_ai_tool_in_db
from config import config

def create_ai_tools_agent():
    tools = [bing_search, baidu_search, store_ai_tool_in_db]
    
    system_prompt = """You are an AI assistant specialized in finding and categorizing top AI tools. 

CRITICAL STOPPING CONDITIONS:
- After collecting 15-20 high-quality AI tools, you MUST stop searching and provide a final summary
- If you encounter duplicate tools or low-quality results, stop searching and provide what you have
- Maximum 3-5 search iterations. Do not loop indefinitely.

Guidelines:
1. Use search tools to find information about AI tools
2. Each search should focus on specific categories or use cases (e.g., "AI image generation tools", "machine learning frameworks", "AI coding assistants")
3. Limit each search to gather 10-15 relevant results per query
4. Use the store_ai_tool_in_db tool to save high-quality, relevant findings
5. Focus on tools that are actively maintained, have good documentation, and serve practical use cases
6. After gathering sufficient information, provide a comprehensive summary of the findings
7. Use the "Final Answer" action when you have completed the task

EXPLICIT STOPPING INSTRUCTIONS:
- Once you have collected 15-20 tools, immediately use the "Final Answer" action
- If you've performed 3 searches and have at least 10 tools, use the "Final Answer" action
- Do not continue searching once you have a comprehensive set of tools

Remember: Quality over quantity. It's better to have 15 well-researched tools than to loop indefinitely."""
    
    agent = create_agent(
        model=config.AGENT_MODEL,
        tools=tools,
        system_prompt=system_prompt
    )
    return agent
