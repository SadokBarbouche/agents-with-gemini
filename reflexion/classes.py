from typing import TypedDict, List
from pydantic import BaseModel

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