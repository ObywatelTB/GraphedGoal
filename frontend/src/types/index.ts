// Types for the GraphedGoal application

// Node in the goal graph
export interface SubgoalNode {
  id: string;
  label: string;
  parent_id: string | null;
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
  created_at: any; // Firebase timestamp
  user_id: string;
}

// For the force-directed graph visualization
export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export interface GraphNode {
  id: string;
  name: string;
  description?: string;
  val?: number; // Size of the node
}

export interface GraphLink {
  source: string;
  target: string;
} 