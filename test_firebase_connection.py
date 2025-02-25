import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def initialize_firebase():
    """Initialize Firebase connection"""
    try:
        # Get the path to the Firebase service account key from .env
        cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

        # Get Firestore client
        db = firestore.client()

        print("✅ Successfully connected to Firebase Firestore!")
        return db
    except Exception as e:
        print(f"❌ Error connecting to Firebase: {str(e)}")
        return None


if __name__ == "__main__":
    print("Testing Firebase connection...")
    db = initialize_firebase()

    if db:
        # Test by listing all collections
        collections = db.collections()
        print("\nAvailable collections:")
        for collection in collections:
            print(f"- {collection.id}")

        print("\nFirebase connection test completed successfully!")
    else:
        print("Failed to establish Firebase connection.")
