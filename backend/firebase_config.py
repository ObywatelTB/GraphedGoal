import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

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


def save_goal_graph(user_id, goal, nodes):
    """Save a goal graph to Firestore."""
    db = initialize_firebase()
    if not db:
        return False

    try:
        # Create a document reference with a generated ID
        doc_ref = db.collection('goal_graphs').document()

        # Set document data
        doc_ref.set({
            'user_id': user_id,
            'goal': goal,
            'nodes': nodes,
            'created_at': firestore.SERVER_TIMESTAMP
        })

        return True
    except Exception as e:
        print(f"Error saving goal graph: {str(e)}")
        return False


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


# Initialize Firebase on module import
db = initialize_firebase()
