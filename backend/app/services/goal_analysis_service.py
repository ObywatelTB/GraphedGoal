import os
import json
import openai
import anthropic
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from app.models.goal import SubgoalNode
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai_client = openai.OpenAI(api_key=openai_api_key)

# Initialize Anthropic client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)


def analyze_goal_for_actions(goal_text: str) -> List[str]:
    """
    First LLM call: Analyze the goal and generate 5-10 proposed actions.

    Args:
        goal_text (str): The main goal to analyze

    Returns:
        List[str]: A list of 5-10 proposed actions to achieve the goal
    """

    # Initialize Google Gemini API
    gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError(
            "GOOGLE_GEMINI_API_KEY environment variable is not set")

    genai.configure(api_key=gemini_api_key)

    prompt = f"""
    Given the following goal: "{goal_text}"
    
    Analyze this goal and suggest 5-10 specific, concrete actions that would help achieve this goal.
    Each action should be clear, actionable, and directly related to the goal.
    
    Your response must clearly depict which actions follow which, to enable presentation as a tree graph.
    Indicate parent-child relationships between actions where appropriate.
    
    The actions must be named in the same language as the original goal query.
    
    Please format your response as a numbered list of actions, one per line.
    """

    # Configure safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    # Call the Gemini API
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config={"temperature": 0.7},
        safety_settings=safety_settings
    )

    response = model.generate_content(prompt)

    # Parse the response to extract the actions
    try:
        content = response.text
        if content is None:
            raise ValueError("Empty response from LLM")

        # Extract the numbered actions from the text response
        # This regex-free approach is more robust for various response formats
        actions = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if line and any(line.startswith(f"{i}.") for i in range(1, 11)):
                # Remove the number and leading/trailing whitespace
                action = line[line.find('.')+1:].strip()
                actions.append(action)
            elif line and not line.startswith('#') and len(actions) < 10:
                # Catch actions that might not be properly numbered
                actions.append(line)

        if not actions:
            raise ValueError("No actions found in LLM response")

        return actions

    except Exception as e:
        raise ValueError(f"Error processing LLM response: {str(e)}")


def create_graph_from_actions(goal_text: str, actions: List[str]) -> List[Dict[str, Any]]:
    """
    Second LLM call: Transform the list of actions into a JSON graph structure.

    Args:
        goal_text (str): The main goal
        actions (List[str]): List of actions from the first LLM

    Returns:
        List[Dict[str, Any]]: A list of nodes representing the graph structure
    """
    # Prepare the actions as a numbered list for the prompt
    actions_text = "\n".join(
        [f"{i+1}. {action}" for i, action in enumerate(actions)])

    prompt = f"""
    Given the following goal: "{goal_text}"
    
    And these proposed actions to achieve it:
    {actions_text}
    
    Create a hierarchical tree graph structure representing how these actions relate to each other.
    Some actions may be prerequisites for others, some may be alternatives, and some may be subtasks.
    
    Format the response as a JSON object with a 'nodes' key containing an array where each node has the following properties:
    - id: A unique string identifier (can be a simple number like "1", "2", etc.)
    - label: A short, descriptive label for the action or subgoal
    - parent_id: The ID of the parent node (null for the root node, which should be the main goal)
    - description: A detailed description of what this action involves
    
    The first node should be the main goal with id "0" and parent_id null.
    The subsequent nodes should represent the actions and any additional steps you think would help organize them logically.
    
    Ensure the tree structure is logical with clear parent-child relationships that make sense for achieving the goal.
    
    Here's an example of the exact JSON format I need:
    
    {{
      "nodes": [
        {{
          "id": "0",
          "label": "Learn Spanish in 6 months",
          "parent_id": null,
          "description": "Master conversational Spanish language skills within a 6-month timeframe"
        }},
        {{
          "id": "1",
          "label": "Establish learning resources",
          "parent_id": "0",
          "description": "Gather necessary learning materials including textbooks, apps, and online courses"
        }},
        {{
          "id": "2",
          "label": "Create study schedule",
          "parent_id": "0",
          "description": "Develop a consistent daily and weekly study plan to ensure regular practice"
        }},
        {{
          "id": "3",
          "label": "Find language exchange partner",
          "parent_id": "0",
          "description": "Connect with native speakers for conversation practice and cultural insights"
        }}
      ]
    }}
    """

    # Call the Anthropic API
    # response = anthropic_client.messages.create(
    #     model="claude-3-5-sonnet-20240620",
    #     max_tokens=4000,
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ],
    #     temperature=0.7,
    #     system="You are a graph structure specialist that organizes actions into logical hierarchical trees."
    # )

    # Implement OpenAI o3-mini
    response = openai_client.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "system", "content": "You are a graph structure specialist that organizes actions into logical hierarchical trees."},
            {"role": "user", "content": prompt}
        ],
        # temperature=0.7,
    )

    # Parse the response
    try:
        # Extract the text content from the response
        content = response.choices[0].message.content

        if not content:
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


def process_goal_with_dual_llm(goal_text: str) -> List[Dict[str, Any]]:
    """
    Process a goal using two LLM calls:
    1. Analyze the goal to get proposed actions
    2. Convert those actions into a graph structure

    Args:
        goal_text (str): The main goal to process

    Returns:
        List[Dict[str, Any]]: A list of nodes representing the graph structure
    """
    # First LLM call to analyze the goal and get actions
    actions = analyze_goal_for_actions(goal_text)

    # Second LLM call to create the graph structure
    nodes = create_graph_from_actions(goal_text, actions)

    # Convert raw dictionaries to SubgoalNode objects and back to dict for consistency
    subgoal_nodes = [SubgoalNode(**node).dict() for node in nodes]

    return subgoal_nodes
