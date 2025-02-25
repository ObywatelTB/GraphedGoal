import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Union

# Load environment variables
load_dotenv()

# Path to Firebase service account key
firebase_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")


def initialize_firebase():
    """Initialize Firebase Admin SDK with the service account key."""
    try:
        if not firebase_key_path:
            print(
                "Warning: FIREBASE_SERVICE_ACCOUNT_KEY environment variable is not set.")
            return None

        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
        return db
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return None


def save_goal_graph(user_id, goal, nodes, graph_id=None):
    """Save a goal graph to Firestore.

    Args:
        user_id (str): The ID of the user who created the goal
        goal (str): The main goal text
        nodes (list): List of subgoal nodes
        graph_id (str, optional): Custom ID for the graph document. If None, a new ID will be generated.

    Returns:
        str: The ID of the created document if successful, None otherwise
    """
    db = initialize_firebase()
    if not db:
        return None

    try:
        # Create a document reference with either the provided ID or a generated one
        if graph_id:
            doc_ref = db.collection('goal_graphs').document(graph_id)
        else:
            doc_ref = db.collection('goal_graphs').document()

        # Set document data
        doc_ref.set({
            'user_id': user_id,
            'goal': goal,
            'nodes': nodes,
            'created_at': firestore.SERVER_TIMESTAMP
        })

        return doc_ref.id
    except Exception as e:
        print(f"Error saving goal graph: {str(e)}")
        return None


def get_user_goal_graphs(user_id):
    """Retrieve all goal graphs for a specific user."""
    db = initialize_firebase()
    if not db:
        return []

    try:
        # Query documents by user_id
        query = db.collection('goal_graphs').where('user_id', '==', user_id).order_by(
            'created_at', direction=firestore.Query.DESCENDING)
        docs = query.stream()

        result = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            result.append(data)

        return result
    except Exception as e:
        print(f"Error retrieving goal graphs: {str(e)}")
        return []


def get_goal_graph_by_id(graph_id):
    """Retrieve a specific goal graph by its ID.

    Args:
        graph_id (str): The ID of the goal graph to retrieve

    Returns:
        dict: The goal graph data if found, None otherwise
    """
    db = initialize_firebase()
    if not db:
        return None

    try:
        # Get document by ID
        doc_ref = db.collection('goal_graphs').document(graph_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        else:
            return None
    except Exception as e:
        print(f"Error retrieving goal graph: {str(e)}")
        return None


def delete_goal_graph(graph_id):
    """Delete a goal graph from Firestore.

    Args:
        graph_id (str): The ID of the goal graph to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    db = initialize_firebase()
    if not db:
        return False

    try:
        # Delete document by ID
        doc_ref = db.collection('goal_graphs').document(graph_id)
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.delete()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting goal graph: {str(e)}")
        return False


def update_goal_graph(graph_id, goal=None, nodes=None):
    """Update an existing goal graph in Firestore.

    Args:
        graph_id (str): The ID of the goal graph to update
        goal (str, optional): The updated main goal text
        nodes (list, optional): Updated list of subgoal nodes

    Returns:
        bool: True if update was successful, False otherwise
    """
    db = initialize_firebase()
    if not db:
        return False

    try:
        # Get document reference
        doc_ref = db.collection('goal_graphs').document(graph_id)
        doc = doc_ref.get()

        if not doc.exists:
            return False

        # Prepare update data
        update_data = {}
        if goal is not None:
            update_data['goal'] = goal
        if nodes is not None:
            update_data['nodes'] = nodes

        # Only update if there's data to update
        if update_data:
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(update_data)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error updating goal graph: {str(e)}")
        return False


# Initialize Firebase on module import
db = initialize_firebase()
