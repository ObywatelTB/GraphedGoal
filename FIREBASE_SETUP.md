# Firebase Setup for GraphedGoal

This document explains how to connect to the Firebase Firestore database for the GraphedGoal project.

## Configuration Setup

1. **Firebase Service Account Key**
   - We have created a service account key file `firebase-credentials.json` for Firebase Admin SDK
   - This key is used for server-side authentication with Firebase

2. **Environment Variables**
   - All Firebase configuration is stored in the `.env` file
   - The file includes:
     - Path to the Firebase service account key
     - Firebase web configuration (API key, project ID, etc.)

## Available Firebase Scripts

### 1. Test Firebase Connection
```
python3 test_firebase_connection.py
```
This simple script verifies the connection to Firebase Firestore and lists available collections.

### 2. Firebase Operations Demo
```
python3 firebase_operations.py
```
This comprehensive script demonstrates:
- Connecting to Firebase Firestore
- Listing collections
- Creating documents
- Reading documents
- Updating documents
- Querying documents
- Deleting documents (for test collections only)

## Firebase Manager Class

We've created a reusable `FirebaseManager` class in `firebase_operations.py` that you can import in your application code:

```python
from firebase_operations import FirebaseManager

# Initialize the Firebase manager
firebase = FirebaseManager()

# Use it for various operations
collections = firebase.list_collections()
document_data = firebase.read_document("collection_name", "document_id")
```

## Firebase Project Details

- **Project Name**: GraphedGoal
- **Project ID**: graphedgoal-app
- **Firestore Database**: Located in us-central1
- **Collections**: goal_trees

## Working with Firebase in Your Application

### Backend (Python)
```python
from firebase_operations import FirebaseManager

firebase = FirebaseManager()
# Use the Firebase manager for database operations
```

### Frontend (JavaScript/React)
In your frontend code, you can use the Firebase Web SDK with the configuration from the `.env` file:

```javascript
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
```

## Security Considerations

- Keep your `.env` file and `firebase-credentials.json` secure and never commit them to public repositories
- The service account has admin access to your Firebase project
- For production, consider setting up Firebase Security Rules to control access to your data 