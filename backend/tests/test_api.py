from main import app
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns the expected message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to GraphedGoal API"}


@patch("openai.OpenAI")
@patch("firebase_config.save_goal_graph")
def test_process_goal_endpoint(mock_save_goal_graph, mock_openai):
    """Test the process-goal endpoint with mocked OpenAI and Firebase."""
    # Mock OpenAI response
    mock_chat_completion = MagicMock()
    mock_chat_completion.choices = [
        MagicMock(
            message=MagicMock(
                content=json.dumps({
                    "nodes": [
                        {
                            "id": "1",
                            "label": "Main Goal",
                            "parent_id": None,
                            "description": "Main goal description"
                        },
                        {
                            "id": "2",
                            "label": "Subgoal 1",
                            "parent_id": "1",
                            "description": "Subgoal 1 description"
                        }
                    ]
                })
            )
        )
    ]

    mock_openai_instance = MagicMock()
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion
    mock_openai.return_value = mock_openai_instance

    # Mock Firebase save
    mock_save_goal_graph.return_value = True

    # Test request with user_id
    payload = {
        "goal": "Learn to play guitar",
        "user_id": "test_user_123"
    }

    response = client.post("/process-goal", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["nodes"]) == 2
    assert response_data["saved"] == True

    # Verify OpenAI was called correctly
    mock_openai_instance.chat.completions.create.assert_called_once()

    # Verify Firebase save was called correctly
    mock_save_goal_graph.assert_called_once_with("test_user_123", "Learn to play guitar", [
        {
            "id": "1",
            "label": "Main Goal",
            "parent_id": None,
            "description": "Main goal description"
        },
        {
            "id": "2",
            "label": "Subgoal 1",
            "parent_id": "1",
            "description": "Subgoal 1 description"
        }
    ])


@patch("firebase_config.get_user_goal_graphs")
def test_get_user_goal_graphs_endpoint(mock_get_user_goal_graphs):
    """Test the get user goal graphs endpoint."""
    # Mock Firebase response
    mock_get_user_goal_graphs.return_value = [
        {
            "id": "graph1",
            "goal": "Learn to play guitar",
            "created_at": "2023-01-01T12:00:00Z",
            "nodes": [
                {
                    "id": "1",
                    "label": "Main Goal",
                    "parent_id": None,
                    "description": "Main goal description"
                }
            ]
        }
    ]

    response = client.get("/user/test_user_123/goal-graphs")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["id"] == "graph1"
    assert response_data[0]["goal"] == "Learn to play guitar"

    # Verify Firebase get was called correctly
    mock_get_user_goal_graphs.assert_called_once_with("test_user_123")
