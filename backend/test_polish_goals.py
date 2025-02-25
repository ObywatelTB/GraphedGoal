from app.services.goal_analysis_service import process_goal_with_dual_llm
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the required modules


def print_node_tree(nodes, node_id="0", level=0):
    """Print the node tree in a hierarchical format."""
    # Find the current node
    current_node = next(
        (node for node in nodes if node["id"] == node_id), None)
    if not current_node:
        return

    # Print the current node with indentation
    indent = "  " * level
    print(f"{indent}└─ {current_node['label']}")
    if current_node.get('description'):
        print(f"{indent}   {current_node['description']}")

    # Find and print all children
    children = [node for node in nodes if node.get('parent_id') == node_id]
    for child in children:
        print_node_tree(nodes, child["id"], level + 1)


def test_polish_goals():
    """Test the goal analysis service with Polish language goals."""
    polish_goals = [
        "Nauczyć się języka hiszpańskiego w 6 miesięcy",
        "Zorganizować rodzinne wakacje w górach",
        "Założyć własny biznes online sprzedający ręcznie robioną biżuterię",
        "Przygotować się do maratonu w 3 miesiące",
        "Napisać i opublikować książkę kucharską z tradycyjnymi przepisami"
    ]

    for i, goal in enumerate(polish_goals, 1):
        print(f"\n\n{'='*80}")
        print(f"TEST {i}: {goal}")
        print(f"{'='*80}\n")

        try:
            # Process the goal
            result = process_goal_with_dual_llm(goal)

            # Print the result as a tree
            print("\nWYNIK (DRZEWO):")
            print_node_tree(result)

            # Print the raw JSON for reference
            print("\nWYNIK (JSON):")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            print(f"\nTest {i} zakończony sukcesem ✓")
        except Exception as e:
            print(f"\nTest {i} zakończony niepowodzeniem ✗")
            print(f"Błąd: {str(e)}")


if __name__ == "__main__":
    print("Rozpoczynam testy analizy celów w języku polskim...\n")
    test_polish_goals()
    print("\nTesty zakończone.")
