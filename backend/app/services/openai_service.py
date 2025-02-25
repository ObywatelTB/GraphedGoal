import os
import json
import openai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai_client = openai.OpenAI(api_key=openai_api_key)


def generate_goal_breakdown(goal_text: str) -> List[Dict[str, Any]]:
    """Generate a breakdown of subgoals for the given goal using OpenAI's API.

    Args:
        goal_text (str): The main goal to break down

    Returns:
        List[Dict[str, Any]]: A list of subgoal nodes
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
        if content is None:
            raise ValueError("Empty response from LLM")
        data = json.loads(content)
        nodes = data.get("nodes", [])

        # Validate the response structure
        for node in nodes:
            if not all(key in node for key in ["id", "label"]):
                raise ValueError("Invalid node structure in LLM response")

        return nodes
    except json.JSONDecodeError:
        raise ValueError("Error parsing LLM response: Invalid JSON format")
    except Exception as e:
        raise ValueError(f"Error processing LLM response: {str(e)}")


def regenerate_goal_breakdown(goal_text: str) -> List[Dict[str, Any]]:
    """Regenerate a breakdown of subgoals for the given goal using OpenAI's API with higher temperature.

    Args:
        goal_text (str): The main goal to break down

    Returns:
        List[Dict[str, Any]]: A list of subgoal nodes
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

    # Call the OpenAI API with higher temperature for more variation
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
        if content is None:
            raise ValueError("Empty response from LLM")
        data = json.loads(content)
        nodes = data.get("nodes", [])

        # Validate the response structure
        for node in nodes:
            if not all(key in node for key in ["id", "label"]):
                raise ValueError("Invalid node structure in LLM response")

        return nodes
    except json.JSONDecodeError:
        raise ValueError("Error parsing LLM response: Invalid JSON format")
    except Exception as e:
        raise ValueError(f"Error processing LLM response: {str(e)}")
