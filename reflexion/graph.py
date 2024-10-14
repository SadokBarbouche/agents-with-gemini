from langgraph.graph import StateGraph
from .nodes import (
    plan_node,
    critique_node,
    generation_node,
    reflection_node,
    research_plan_node,
    should_continue,
)
from langgraph.graph import END
from .classes import AgentState
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables.base import ensure_config


graph = StateGraph(AgentState)

graph.add_node("planner", plan_node)
graph.add_node("generate", generation_node)
graph.add_node("reflect", reflection_node)
graph.add_node("research_plan", research_plan_node)
graph.add_node("research_critique", critique_node)
graph.set_entry_point("planner")

graph.add_edge("planner", "research_plan")
graph.add_edge("research_plan", "generate")
graph.add_conditional_edges(
    "generate", should_continue, {END: END, "reflect": "reflect"}
)
graph.add_edge("reflect", "research_critique")
graph.add_edge("research_critique", "generate")

if __name__ == "__main__":
    with SqliteSaver.from_conn_string(":memory:") as checkpointer:
        graph = graph.compile(checkpointer=checkpointer)
        # with open("reflexion_graph.png", "wb") as f:
        #     f.write(graph.get_graph().draw_mermaid_png())
        thread = {"configurable": {"thread_id": "1"}}
        task = "Write an essay about Agentic Workflows using Langchain and Langgraph"
        prompt = {"task": task, "max_revision": 2, "revision_number": 1}
        events = graph.stream(prompt, thread)
        for e in events:
            print(e)
            print('-' * 100)