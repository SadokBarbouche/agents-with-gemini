from typing import TypedDict
from langchain_core.pydantic_v1 import BaseModel
from typing import List

class AgentState(TypedDict):
    task : str
    plan : str
    draft : str
    critique : str
    content : List[str]
    revision_number : int
    max_revision : int

class Queries(BaseModel):
    queries : List[str]