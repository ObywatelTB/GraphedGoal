from pydantic import BaseModel
from typing import List, Optional


class GoalRequest(BaseModel):
    goal: str
    user_id: Optional[str] = None


class SubgoalNode(BaseModel):
    id: str
    label: str
    parent_id: Optional[str] = None
    description: Optional[str] = None


class GoalGraphResponse(BaseModel):
    nodes: List[SubgoalNode]
    saved: bool = False
    graph_id: Optional[str] = None


class GoalGraphUpdateRequest(BaseModel):
    goal: Optional[str] = None
    nodes: Optional[List[SubgoalNode]] = None
