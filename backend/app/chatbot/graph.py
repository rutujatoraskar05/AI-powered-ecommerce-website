from chatbot.agents.ecommerce_agent import get_agent

agent = None


async def initialize_agent():

    global agent

    if agent is None:
        agent = await get_agent()

    return agent


async def run_chat(message: str):

    current_agent = await initialize_agent()

    result = await current_agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    message
                )
            ]
        }
    )

    return result["messages"][-1].content