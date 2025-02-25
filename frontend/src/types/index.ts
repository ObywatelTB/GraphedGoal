// Types for the GraphedGoal application

// Node in the goal graph
export interface SubgoalNode {
  id: string;
  label: string;
  parent_id?: string | null;
  description?: string;
}

// Response from the API when processing a goal
export interface GoalGraphResponse {
  nodes: SubgoalNode[];
  saved: boolean;
  graph_id?: string;
}

// Request to process a goal
export interface GoalRequest {
  goal: string;
  user_id?: string;
}

// Saved goal graph from Firebase
export interface SavedGoalGraph {
  id: string;
  goal: string;
  nodes: SubgoalNode[];
  created_at: Timestamp;
  user_id: string;
}

// For the force-directed graph visualization
export interface GraphData {
  nodes: Array<{
    id: string;
    name: string;
    description?: string;
    val?: number;
  }>;
  links: Array<{
    source: string;
    target: string;
  }>;
}

// Timestamp type for Firestore
export interface Timestamp {
  seconds: number;
  nanoseconds: number;
}

// User profile type
export interface UserProfile {
  uid: string;
  email: string;
  displayName?: string;
} 