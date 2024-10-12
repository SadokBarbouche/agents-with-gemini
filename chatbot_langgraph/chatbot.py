from .graph import graph

config = {"configurable": {"thread_id": "1"}}

# with open("graph_image.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())

while True:
    user_input = input("User : ")
    if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
        print("Goodbye!")
        exit(0)
    for event in graph.stream({"messages": [user_input]}, config):
        for value in event.values():
            print(f"Assistant : {value['messages'][-1].content}")
            print("-" * 100)
