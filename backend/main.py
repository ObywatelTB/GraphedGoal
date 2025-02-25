import os
from fastapi import FastAPI, HTTPException, Depends  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from pydantic import BaseModel  # type: ignore
from dotenv import load_dotenv  # type: ignore
import openai  # type: ignore
from typing import List, Dict, Any, Optional, Union
import json
import uuid

# Firebase integration
from . import firebase_config

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai_client = openai.OpenAI(api_key=openai_api_key)

app = FastAPI(title="GraphedGoal API",
              description="API for goal visualization and planning")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input and output models


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


@app.get("/")
async def root():
    return {"message": "Welcome to GraphedGoal API"}


@app.post("/process-goal", response_model=GoalGraphResponse)
async def process_goal(request: GoalRequest):
    try:
        # Validate input
        if not request.goal or len(request.goal.strip()) == 0:
            raise HTTPException(status_code=400, detail="Goal cannot be empty")

        # Create prompt for the LLM
        prompt = f"""
        Given the following goal: "{request.goal}"
        
        Break down this goal into a tree of 5-15 subgoals and steps.
        
        Format the response as a JSON object with a 'nodes' key containing an array where each node has the following properties:
        - id: A unique string identifier
        - label: A short, descriptive label for the subgoal
        - parent_id: The ID of the parent node (null for the root node)
        - description: A detailed description of what this subgoal involves
        
        Ensure the tree structure is logical with clear parent-child relationships.
        """

        # Call the OpenAI API
        response = openai_client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a goal planning assistant that helps break down goals into achievable subgoals and steps."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        # Parse the response
        try:
            content = response.choices[0].message.content
            data = json.loads(content)
            nodes = data.get("nodes", [])

            # Validate the response structure
            for node in nodes:
                if not all(key in node for key in ["id", "label"]):
                    raise ValueError("Invalid node structure in LLM response")

            # Save to Firebase if user_id is provided
            saved = False
            graph_id = None

            if request.user_id:
                # Generate a unique ID for the graph
                graph_id = str(uuid.uuid4())

                # Save to Firebase and get the document ID
                saved_graph_id = firebase_config.save_goal_graph(
                    request.user_id, request.goal, nodes, graph_id)

                # If saving was successful, update the saved flag
                if saved_graph_id:
                    saved = True
                    graph_id = saved_graph_id
                else:
                    graph_id = None

            return {"nodes": nodes, "saved": saved, "graph_id": graph_id}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500, detail="Error parsing LLM response: Invalid JSON format")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing LLM response: {str(e)}")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/user/{user_id}/goal-graphs", response_model=List[Dict[str, Any]])
async def get_user_goal_graphs(user_id: str):
    try:
        graphs = firebase_config.get_user_goal_graphs(user_id)
        return graphs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/goal-graph/{graph_id}", response_model=Dict[str, Any])
async def get_goal_graph(graph_id: str):
    """Retrieve a specific goal graph by its ID."""
    try:
        graph = firebase_config.get_goal_graph_by_id(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="Goal graph not found")
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/goal-graph/{graph_id}")
async def delete_goal_graph(graph_id: str):
    """Delete a specific goal graph by its ID."""
    try:
        success = firebase_config.delete_goal_graph(graph_id)
        if not success:
            raise HTTPException(
                status_code=404, detail="Goal graph not found or could not be deleted")
        return {"message": "Goal graph deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/goal-graph/{graph_id}")
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

        success = firebase_config.update_goal_graph(
            graph_id, request.goal, nodes_dict)
        if not success:
            raise HTTPException(
                status_code=404, detail="Goal graph not found or could not be updated")

        return {"message": "Goal graph updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/goal-graph/{graph_id}/regenerate", response_model=GoalGraphResponse)
async def regenerate_goal_graph(graph_id: str):
    """Regenerate subgoals for an existing goal using the LLM."""
    try:
        # Get the existing goal graph
        graph = firebase_config.get_goal_graph_by_id(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="Goal graph not found")

        goal_text = graph.get("goal")
        user_id = graph.get("user_id")

        if not goal_text:
            raise HTTPException(
                status_code=400, detail="Goal text not found in the existing graph")

        # Create prompt for the LLM
        prompt = f"""
        Given the following goal: "{goal_text}"
        
        Break down this goal into a tree of 5-15 subgoals and steps.
        
        Format the response as a JSON object with a 'nodes' key containing an array where each node has the following properties:
        - id: A unique string identifier
        - label: A short, descriptive label for the subgoal
        - parent_id: The ID of the parent node (null for the root node)
        - description: A detailed description of what this subgoal involves
        
        Ensure the tree structure is logical with clear parent-child relationships.
        """

        # Call the OpenAI API
        response = openai_client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are a goal planning assistant that helps break down goals into achievable subgoals and steps."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.9,  # Higher temperature for more variation
        )

        # Parse the response
        try:
            content = response.choices[0].message.content
            data = json.loads(content)
            nodes = data.get("nodes", [])

            # Validate the response structure
            for node in nodes:
                if not all(key in node for key in ["id", "label"]):
                    raise ValueError("Invalid node structure in LLM response")

            # Update the existing goal graph with new nodes
            success = firebase_config.update_goal_graph(graph_id, None, nodes)

            return {"nodes": nodes, "saved": success, "graph_id": graph_id if success else None}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500, detail="Error parsing LLM response: Invalid JSON format")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing LLM response: {str(e)}")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    import uvicorn  # type: ignore
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
