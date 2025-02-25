from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class SubgoalNode(BaseModel):
    """Model for a subgoal node in the goal graph."""
    id: str
    label: str
    parent_id: Optional[str] = None
    description: Optional[str] = None


class GoalRequest(BaseModel):
    """Model for a goal processing request."""
    goal: str
    user_id: Optional[str] = None


class GoalGraphResponse(BaseModel):
    """Model for a goal graph response."""
    nodes: List[SubgoalNode]
    saved: bool = False
    graph_id: Optional[str] = None


class GoalGraphUpdateRequest(BaseModel):
    """Model for a goal graph update request."""
    goal: Optional[str] = None
    nodes: Optional[List[SubgoalNode]] = None
