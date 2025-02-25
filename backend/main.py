import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any, Optional, Union
import json
import uuid

# Firebase integration
import firebase_config

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


@app.get("/")
async def root():
    return {"message": "Welcome to GraphedGoal API"}


@app.post("/process-goal", response_model=GoalGraphResponse)
async def process_goal(request: GoalRequest):
    try:
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
                # Save to Firebase
                saved = firebase_config.save_goal_graph(
                    request.user_id, request.goal, nodes)

            return {"nodes": nodes, "saved": saved, "graph_id": graph_id}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error parsing LLM response: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/goal-graphs", response_model=List[Dict[str, Any]])
async def get_user_goal_graphs(user_id: str):
    try:
        graphs = firebase_config.get_user_goal_graphs(user_id)
        return graphs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
