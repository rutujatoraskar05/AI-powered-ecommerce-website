from langgraph.prebuilt import create_react_agent

from chatbot.llm import llm
from chatbot.prompts.ecommerce_prompt import SYSTEM_PROMPT

from langchain_mcp_adapters.client import MultiServerMCPClient


client = MultiServerMCPClient(

    {
        "product": {

            "command": "python",
            "args": ["chatbot/mcp_servers/product_tools.py"],
            "transport": "stdio",
        },

        "review": {

            "command": "python",
            "args": ["chatbot/mcp_servers/review_tools.py"],
            "transport": "stdio",
        },

        "mysql": {

            "command": "python",
            "args": ["chatbot/mcp_servers/mysql_tools.py"],

            "transport": "stdio",
        },

        "cart": {

            "command": "python",
            "args": ["chatbot/mcp_servers/cart_tools.py"],

            "transport": "stdio",
        },

        "wishlist": {

            "command": "python",
            "args": ["chatbot/mcp_servers/wishlist_tools.py"],

            "transport": "stdio",
        },

        "orders": {

            "command": "python",
            "args": ["chatbot/mcp_servers/order_tools.py"],

            "transport": "stdio",
        },
            "profile": {

            "command": "python",
            "args": ["chatbot/mcp_servers/profile_tools.py"],
             "transport": "stdio",
        }
    }

)


async def get_agent():

    tools = await client.get_tools()

    agent = create_react_agent(

        model=llm,

        tools=tools,

        prompt=SYSTEM_PROMPT,

    )

    return agent