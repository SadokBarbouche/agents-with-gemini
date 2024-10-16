from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from react import get_client
from langgraph.checkpoint.memory import MemorySaver

# add_messages:
# import operator
# add_messages = operator.add

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = get_client()

graph_builder = StateGraph(State)

def chatbot(state: State):
    print(state["messages"])
    return {"messages": [llm.invoke(state["messages"])]}

memory = MemorySaver()

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")

graph = graph_builder.compile(checkpointer=memory)