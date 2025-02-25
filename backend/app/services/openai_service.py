import json
import openai
from ..core.config import settings
from ..models.goal import SubgoalNode, GoalGraphResponse
from typing import List, Dict, Any


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        """Initialize the OpenAI client."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate_goal_graph(self, goal_text: str) -> List[Dict[str, Any]]:
        """Generate a goal graph using OpenAI's LLM.

        Args:
            goal_text: The main goal to break down

        Returns:
            List of subgoal nodes

        Raises:
            ValueError: If the LLM response is invalid
            Exception: For other errors
        """
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a goal planning assistant that helps break down goals into achievable subgoals and steps."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        # Parse the response
        content = response.choices[0].message.content
        data = json.loads(content)
        nodes = data.get("nodes", [])

        # Validate the response structure
        for node in nodes:
            if not all(key in node for key in ["id", "label"]):
                raise ValueError("Invalid node structure in LLM response")

        return nodes

    def regenerate_goal_graph(self, goal_text: str) -> List[Dict[str, Any]]:
        """Regenerate a goal graph with higher temperature for more variation.

        Args:
            goal_text: The main goal to break down

        Returns:
            List of subgoal nodes

        Raises:
            ValueError: If the LLM response is invalid
            Exception: For other errors
        """
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

        # Call the OpenAI API with higher temperature
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a goal planning assistant that helps break down goals into achievable subgoals and steps."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.9,  # Higher temperature for more variation
        )

        # Parse the response
        content = response.choices[0].message.content
        data = json.loads(content)
        nodes = data.get("nodes", [])

        # Validate the response structure
        for node in nodes:
            if not all(key in node for key in ["id", "label"]):
                raise ValueError("Invalid node structure in LLM response")

        return nodes


# Create a singleton instance
openai_service = OpenAIService()
