import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, User } from 'firebase/auth';
import { getFirestore, collection, doc, setDoc, getDoc, getDocs, query, where, orderBy, Timestamp } from 'firebase/firestore';
import { SavedGoalGraph } from '../types';

// Firebase configuration from environment variables
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
const auth = getAuth(app);
const db = getFirestore(app);

// Authentication functions
export const firebaseAuth = {
  // Sign in with email and password
  signIn: (email: string, password: string) => {
    return signInWithEmailAndPassword(auth, email, password);
  },

  // Register a new user
  register: (email: string, password: string) => {
    return createUserWithEmailAndPassword(auth, email, password);
  },

  // Sign out
  signOut: () => {
    return signOut(auth);
  },

  // Get current user
  getCurrentUser: (): User | null => {
    return auth.currentUser;
  }
};

// Firestore functions
export const firebaseFirestore = {
  // Save a goal graph
  saveGoalGraph: async (userId: string, goal: string, nodes: any[]): Promise<string> => {
    try {
      const goalGraphsRef = collection(db, 'goal_graphs');
      const docRef = doc(goalGraphsRef);
      
      await setDoc(docRef, {
        user_id: userId,
        goal,
        nodes,
        created_at: Timestamp.now()
      });
      
      return docRef.id;
    } catch (error) {
      console.error('Error saving goal graph:', error);
      throw error;
    }
  },

  // Get all goal graphs for a user
  getUserGoalGraphs: async (userId: string): Promise<SavedGoalGraph[]> => {
    try {
      const goalGraphsRef = collection(db, 'goal_graphs');
      const q = query(
        goalGraphsRef, 
        where('user_id', '==', userId),
        orderBy('created_at', 'desc')
      );
      
      const querySnapshot = await getDocs(q);
      const goalGraphs: SavedGoalGraph[] = [];
      
      querySnapshot.forEach((doc) => {
        const data = doc.data();
        goalGraphs.push({
          id: doc.id,
          goal: data.goal,
          nodes: data.nodes,
          created_at: data.created_at,
          user_id: data.user_id
        });
      });
      
      return goalGraphs;
    } catch (error) {
      console.error('Error getting user goal graphs:', error);
      throw error;
    }
  }
};

export default { auth, db, firebaseAuth, firebaseFirestore }; 