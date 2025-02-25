import axios from 'axios';
import { GoalRequest, GoalGraphResponse, SavedGoalGraph } from '../types';

// Get the API URL from environment variables or use default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with base URL
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service functions
export const apiService = {
  // Process a goal and get subgoals
  processGoal: async (request: GoalRequest): Promise<GoalGraphResponse> => {
    try {
      const response = await apiClient.post<GoalGraphResponse>('/process-goal', request);
      return response.data;
    } catch (error) {
      console.error('Error processing goal:', error);
      throw error;
    }
  },

  // Get all goal graphs for a user
  getUserGoalGraphs: async (userId: string): Promise<SavedGoalGraph[]> => {
    try {
      const response = await apiClient.get<SavedGoalGraph[]>(`/user/${userId}/goal-graphs`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user goal graphs:', error);
      throw error;
    }
  },

  // Health check
  healthCheck: async (): Promise<{ message: string }> => {
    try {
      const response = await apiClient.get<{ message: string }>('/');
      return response.data;
    } catch (error) {
      console.error('API health check failed:', error);
      throw error;
    }
  },
}; 