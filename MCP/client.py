from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
client = MultiServerMCPClient(
    {
        "Math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio",
        },
        "Weather": {
            "command": "python",
            "args": ["weather.py"],
            "transport": "stdio",
        },
    }
)
import os
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("GROQ_API_KEY not found in .env file")
os.environ["GROQ_API_KEY"] = groq_key

async def main():
    tools = await client.get_tools()
    model= ChatGroq(model="moonshotai/kimi-k2-instruct-0905", temperature=0)
    agent = create_react_agent(
        model, tools)
    math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "What is 15 plus 27 multiplied by 3?"}]}
    )
    print("Math Response:", math_response['messages'][-1].content)

asyncio.run(main())
