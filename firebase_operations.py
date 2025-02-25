import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()


class FirebaseManager:
    """Class to manage Firebase Firestore operations"""

    def __init__(self):
        """Initialize Firebase connection"""
        try:
            # Get the path to the Firebase service account key from .env
            cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

            # Initialize Firebase Admin SDK (if not already initialized)
            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)

            # Get Firestore client
            self.db = firestore.client()
            print("✅ Successfully connected to Firebase Firestore!")
        except Exception as e:
            print(f"❌ Error connecting to Firebase: {str(e)}")
            self.db = None

    def list_collections(self):
        """List all collections in the database"""
        if not self.db:
            return []

        collections = self.db.collections()
        return [collection.id for collection in collections]

    def create_document(self, collection_name, data, doc_id=None):
        """Create a new document in the specified collection"""
        if not self.db:
            return None

        try:
            collection_ref = self.db.collection(collection_name)

            # If no doc_id is provided, generate one or let Firestore auto-generate it
            if doc_id:
                doc_ref = collection_ref.document(doc_id)
                doc_ref.set(data)
            else:
                # add() returns (None, doc_reference)
                doc_ref = collection_ref.add(data)[1]

            print(
                f"✅ Document created successfully in {collection_name} collection!")
            return doc_ref.id
        except Exception as e:
            print(f"❌ Error creating document: {str(e)}")
            return None

    def read_document(self, collection_name, doc_id):
        """Read a document from the specified collection"""
        if not self.db:
            return None

        try:
            doc_ref = self.db.collection(collection_name).document(doc_id)
            doc = doc_ref.get()

            if doc.exists:
                print(f"✅ Document {doc_id} retrieved successfully!")
                return doc.to_dict()
            else:
                print(f"⚠️ Document {doc_id} does not exist!")
                return None
        except Exception as e:
            print(f"❌ Error reading document: {str(e)}")
            return None

    def update_document(self, collection_name, doc_id, data):
        """Update a document in the specified collection"""
        if not self.db:
            return False

        try:
            doc_ref = self.db.collection(collection_name).document(doc_id)
            doc_ref.update(data)
            print(f"✅ Document {doc_id} updated successfully!")
            return True
        except Exception as e:
            print(f"❌ Error updating document: {str(e)}")
            return False

    def delete_document(self, collection_name, doc_id):
        """Delete a document from the specified collection"""
        if not self.db:
            return False

        try:
            doc_ref = self.db.collection(collection_name).document(doc_id)
            doc_ref.delete()
            print(f"✅ Document {doc_id} deleted successfully!")
            return True
        except Exception as e:
            print(f"❌ Error deleting document: {str(e)}")
            return False

    def query_documents(self, collection_name, field, operator, value):
        """Query documents from a collection based on a field condition"""
        if not self.db:
            return []

        try:
            query_ref = self.db.collection(
                collection_name).where(field, operator, value)
            docs = query_ref.stream()

            results = []
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data['id'] = doc.id
                results.append(doc_data)

            print(
                f"✅ Query executed successfully! Found {len(results)} documents.")
            return results
        except Exception as e:
            print(f"❌ Error querying documents: {str(e)}")
            return []


def demo_firebase_operations():
    """Demonstrate Firebase Firestore operations"""
    # Initialize Firebase manager
    firebase = FirebaseManager()

    # List collections
    print("\n1. Listing collections...")
    collections = firebase.list_collections()
    print(f"Available collections: {collections}")

    # Check if the goal_trees collection exists, otherwise create a test_collection
    collection_name = "goal_trees" if "goal_trees" in collections else "test_collection"
    print(f"\nUsing collection: {collection_name}")

    # Create a document
    print("\n2. Creating a document...")
    new_goal = {
        "title": "Learn Firebase",
        "description": "Master Firebase Firestore database operations",
        "created_at": datetime.now(),
        "completed": False,
        # Adding a unique ID to ensure this is a test document
        "test_id": str(uuid.uuid4())
    }
    doc_id = firebase.create_document(collection_name, new_goal)

    if doc_id:
        # Read the document
        print("\n3. Reading the document...")
        retrieved_doc = firebase.read_document(collection_name, doc_id)
        print(f"Retrieved document: {retrieved_doc}")

        # Update the document
        print("\n4. Updating the document...")
        update_data = {
            "completed": True,
            "updated_at": datetime.now()
        }
        firebase.update_document(collection_name, doc_id, update_data)

        # Read the updated document
        print("\n5. Reading the updated document...")
        updated_doc = firebase.read_document(collection_name, doc_id)
        print(f"Updated document: {updated_doc}")

        # Query documents
        print("\n6. Querying documents...")
        query_results = firebase.query_documents(
            collection_name, "completed", "==", True)
        print(f"Query results: {query_results}")

        # Delete the document if this is a test_collection
        if collection_name == "test_collection":
            print("\n7. Deleting the document...")
            firebase.delete_document(collection_name, doc_id)
        else:
            print("\n7. Skipping deletion for production collection...")


if __name__ == "__main__":
    print("Firebase Firestore Operations Demo")
    print("==================================")
    demo_firebase_operations()
