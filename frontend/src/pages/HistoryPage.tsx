import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { SavedGoalGraph, SubgoalNode } from '../types';
import GoalGraph from '../components/GoalGraph';

// Mock user ID for demo purposes
const DEMO_USER_ID = 'demo-user-123';

const HistoryPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [goalGraphs, setGoalGraphs] = useState<SavedGoalGraph[]>([]);
  const [selectedGraph, setSelectedGraph] = useState<SavedGoalGraph | null>(null);

  useEffect(() => {
    const fetchGoalGraphs = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const graphs = await apiService.getUserGoalGraphs(DEMO_USER_ID);
        setGoalGraphs(graphs);
        
        // Select the first graph by default if available
        if (graphs.length > 0) {
          setSelectedGraph(graphs[0]);
        }
      } catch (err) {
        console.error('Error fetching goal graphs:', err);
        setError('Failed to load your saved goal graphs. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchGoalGraphs();
  }, []);

  const handleSelectGraph = (graph: SavedGoalGraph) => {
    setSelectedGraph(graph);
  };

  const formatDate = (timestamp: any) => {
    if (!timestamp) return 'Unknown date';
    
    // Firebase timestamp handling
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="history-page">
      <div className="container">
        <h1>Your Goal History</h1>
        
        {isLoading && (
          <div className="loading-section">
            <p>Loading your saved goals...</p>
            <div className="spinner"></div>
          </div>
        )}
        
        {error && (
          <div className="error-section">
            <p>{error}</p>
          </div>
        )}
        
        {!isLoading && !error && goalGraphs.length === 0 && (
          <div className="empty-state">
            <p>You don't have any saved goals yet. Create your first goal on the home page!</p>
          </div>
        )}
        
        {goalGraphs.length > 0 && (
          <div className="history-content">
            <div className="goal-list">
              <h2>Saved Goals</h2>
              <ul>
                {goalGraphs.map((graph) => (
                  <li 
                    key={graph.id} 
                    className={selectedGraph?.id === graph.id ? 'selected' : ''}
                    onClick={() => handleSelectGraph(graph)}
                  >
                    <h3>{graph.goal}</h3>
                    <p className="date">{formatDate(graph.created_at)}</p>
                  </li>
                ))}
              </ul>
            </div>
            
            {selectedGraph && (
              <div className="selected-goal">
                <h2>{selectedGraph.goal}</h2>
                <p className="date">Created on {formatDate(selectedGraph.created_at)}</p>
                <GoalGraph nodes={selectedGraph.nodes as SubgoalNode[]} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage; 