from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.llms import OpenAI # Placeholder, actual model will be configured
from ..tools.search_tools import google_search, bing_search, baidu_search
from ..tools.db_tools import store_ai_tool_in_db

def create_ai_tools_agent():
    tools = [google_search, bing_search, baidu_search, store_ai_tool_in_db]

    # Placeholder for LLM - Replace with actual LLM configuration (e.g., Gemini, DeepSeek)
    # For now, we'll use OpenAI as a placeholder. You'll need to set OPENAI_API_KEY environment variable.
    llm = OpenAI(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant that helps find and categorize top AI tools. "
                   "Use the available search tools to find information and the store_ai_tool_in_db tool to save relevant findings."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
