from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import uuid

from ...models.goal import GoalRequest, GoalGraphResponse, GoalGraphUpdateRequest, SubgoalNode
from ...services.openai_service import openai_service
from ...db.firebase import firebase_client

router = APIRouter()


@router.post("/process-goal", response_model=GoalGraphResponse)
async def process_goal(request: GoalRequest):
    """Process a goal and generate a graph of subgoals."""
    try:
        # Validate input
        if not request.goal or len(request.goal.strip()) == 0:
            raise HTTPException(status_code=400, detail="Goal cannot be empty")

        # Generate goal graph using OpenAI
        try:
            nodes = openai_service.generate_goal_graph(request.goal)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error generating goal graph: {str(e)}")

        # Save to Firebase if user_id is provided
        saved = False
        graph_id = None

        if request.user_id:
            # Generate a unique ID for the graph
            graph_id = str(uuid.uuid4())

            # Save to Firebase and get the document ID
            saved_graph_id = firebase_client.save_goal_graph(
                request.user_id, request.goal, nodes, graph_id)

            # If saving was successful, update the saved flag
            if saved_graph_id:
                saved = True
                graph_id = saved_graph_id
            else:
                graph_id = None

        return {"nodes": nodes, "saved": saved, "graph_id": graph_id}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/user/{user_id}/goal-graphs", response_model=List[Dict[str, Any]])
async def get_user_goal_graphs(user_id: str):
    """Retrieve all goal graphs for a specific user."""
    try:
        graphs = firebase_client.get_user_goal_graphs(user_id)
        return graphs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/goal-graph/{graph_id}", response_model=Dict[str, Any])
async def get_goal_graph(graph_id: str):
    """Retrieve a specific goal graph by its ID."""
    try:
        graph = firebase_client.get_goal_graph_by_id(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="Goal graph not found")
        return graph
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/goal-graph/{graph_id}")
async def delete_goal_graph(graph_id: str):
    """Delete a specific goal graph by its ID."""
    try:
        success = firebase_client.delete_goal_graph(graph_id)
        if not success:
            raise HTTPException(
                status_code=404, detail="Goal graph not found or could not be deleted")
        return {"message": "Goal graph deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/goal-graph/{graph_id}")
async def update_goal_graph(graph_id: str, request: GoalGraphUpdateRequest):
    """Update a specific goal graph by its ID."""
    try:
        # Validate that at least one field is provided
        if request.goal is None and request.nodes is None:
            raise HTTPException(
                status_code=400, detail="At least one field (goal or nodes) must be provided")

        # Convert nodes to dict if provided
        nodes_dict = None
        if request.nodes is not None:
            nodes_dict = [node.dict() for node in request.nodes]

            # Validate the nodes structure
            for node in nodes_dict:
                if not all(key in node for key in ["id", "label"]):
                    raise ValueError("Invalid node structure in request")

        success = firebase_client.update_goal_graph(
            graph_id, request.goal, nodes_dict)
        if not success:
            raise HTTPException(
                status_code=404, detail="Goal graph not found or could not be updated")

        return {"message": "Goal graph updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/goal-graph/{graph_id}/regenerate", response_model=GoalGraphResponse)
async def regenerate_goal_graph(graph_id: str):
    """Regenerate subgoals for an existing goal using the LLM."""
    try:
        # Get the existing goal graph
        graph = firebase_client.get_goal_graph_by_id(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="Goal graph not found")

        goal_text = graph.get("goal")
        user_id = graph.get("user_id")

        if not goal_text:
            raise HTTPException(
                status_code=400, detail="Goal text not found in the existing graph")

        # Generate new goal graph using OpenAI
        try:
            nodes = openai_service.regenerate_goal_graph(goal_text)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error regenerating goal graph: {str(e)}")

        # Update the existing graph in Firebase
        success = firebase_client.update_goal_graph(graph_id, None, nodes)

        return {"nodes": nodes, "saved": success, "graph_id": graph_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")
