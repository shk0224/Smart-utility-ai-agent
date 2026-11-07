"""OpenAI tool-calling agent and its execution trace."""
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from tools import ALL_TOOLS

load_dotenv()


def run_agent(question: str) -> dict:
    """Send the user question to the agent and collect tool calls/results."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=(
            "You are a helpful utility assistant. Use the available tools for calculations "
            "instead of doing arithmetic yourself. Use multiple tools if necessary. "
            "Ask for missing inputs instead of inventing them. "
            "Dates must be YYYY-MM-DD. Convert provided units to the tool's expected units. "
            "For age without an as-of date, leave as_of_date empty. "
            "BMI categories apply to adults and are not medical diagnoses. "
            "For percentages, express them using arithmetic, e.g. 15% of 200 = 15/100*200."
        ),
    )
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    trace = []
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                trace.append({"type": "tool_call", "tool": call["name"], "arguments": call["args"]})
        elif isinstance(message, ToolMessage):
            trace.append({"type": "tool_result", "tool": message.name, "result": str(message.content)})

    final = result["messages"][-1].content
    return {"answer": final if isinstance(final, str) else str(final), "trace": trace}
