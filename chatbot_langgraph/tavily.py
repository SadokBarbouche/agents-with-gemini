from tavily import TavilyClient
import os

client = TavilyClient(
    api_key=os.environ.get("TAVILY_API_KEY"),
)

response = client.search(
    query="Who is Sadok Barbouche that studies at INSAT ?",
    search_depth='advanced',
    max_results=1,
    include_images=True,
    include_raw_content=False,
    include_answer=True
)

print(response["answer"] + "\n" + "_" * 50)

answer = client.qna_search("Who is the actual president of Tunisia ?")

print(answer)