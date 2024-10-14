from .classes import AgentState, Queries
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ChatMessage,
    SystemMessage,
    AnyMessage,
)
from .prompts import (
    PLAN_PROMPT,
    WRITER_PROMPT,
    REFLECTION_PROMPT,
    RESEARCH_PLAN_PROMPT,
    RESEARCH_CRITIQUE_PROMPT,
)
from langgraph.graph import END
from react import get_client
from tavily import TavilyClient
import os

model = get_client()

tavily_client = TavilyClient(
    api_key=os.environ.get("TAVILY_API_KEY"),
)

def plan_node(state: AgentState):
    messages = [SystemMessage(PLAN_PROMPT), HumanMessage(content=state["task"])]
    response = model.invoke(messages)
    return {"plan": response}


def research_plan_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke(
        [
            SystemMessage(content=RESEARCH_PLAN_PROMPT),
            HumanMessage(content=state["task"]),
        ]
    )
    content = []
    if 'content' in state:
        content = state["content"]
    if queries:
        for q in queries:
            response = tavily_client.search(query=q, max_results=2)
            for r in response["results"]:
                content.append(r['content'])
    return {"content": content}


def generation_node(state: AgentState):
    content = "\n".join(state["content"] or [])
    user_message = HumanMessage(
        content=f"{state['task']}\nHere is my plan\n{state['plan']}"
    )
    messages = [
        SystemMessage(content=WRITER_PROMPT.format(content=content)),
        user_message,
    ]
    response = model.invoke(messages)
    return {"draft": response, "revision_number": state.get("revision_number", 1) + 1}


def reflection_node(state: AgentState):
    messages = [
        SystemMessage(content=REFLECTION_PROMPT),
        HumanMessage(content=state["draft"]),
    ]
    response = model.invoke(messages)
    return {"crititque": response}


def critique_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke(
        [
            SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
            HumanMessage(content=state["critque"]),
        ]
    )
    content = []
    if 'content' in state:
        content = state["content"]
    for q in queries:
        response = tavily_client.search(query=q, max_results=2)
        for r in response["results"]:
            content.append(r["content"])
    return {"content": content}


def should_continue(state: AgentState):
    if state["revision_number"] > state["max_revision"]:
        return END
    return "reflect"
