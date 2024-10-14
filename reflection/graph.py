from typing import List, Sequence
from langgraph.graph import END, MessageGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from reflection.generate import request, generation_chain
from react import get_client
from reflection.reflect_and_repeat import reflection_prompt

llm = get_client()

reflection_chain = reflection_prompt | llm | StrOutputParser()

def generation_node(state: Sequence[BaseMessage]):
    return generation_chain.invoke({"messages": state})

def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    cls_map = {
        'ai': AIMessage,
        'human': HumanMessage
    }
    # The first message is the original user request, we keep it the same in all the nodes
    translated = [messages[0]] + [cls_map[msg.type](content=msg.content) for msg in messages[1:]]
    result = reflection_chain.invoke({"messages": translated})
    return [HumanMessage(content=result)]

def should_continue(state: List[BaseMessage], MAX_ITER=6):
    if len(state) > MAX_ITER:
        return END
    return 'reflect'

builder = MessageGraph()
builder.add_node('generate', generation_node)
builder.add_node('reflect', reflection_node)
builder.set_entry_point('generate')
builder.add_conditional_edges('generate', should_continue)
builder.add_edge('reflect', 'generate')
graph = builder.compile()

# with open("reflection_graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())

message = HumanMessage(
            content="Generate a tweet about Tunisia winning Africa Cup 2004."
        )

if __name__ == '__main__':
    response = graph.invoke(message)
    for res in response:
        print(res)
