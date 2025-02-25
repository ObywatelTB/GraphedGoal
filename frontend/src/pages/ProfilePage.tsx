import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import { apiService } from '../services/api';
import GoalGraph from '../components/GoalGraph';
import { SavedGoalGraph } from '../types';

const ProfilePage: React.FC = () => {
  const { currentUser, isLoading: authLoading, logout } = useUser();
  const [savedGraphs, setSavedGraphs] = useState<SavedGoalGraph[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedGraph, setSelectedGraph] = useState<SavedGoalGraph | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!authLoading && !currentUser) {
      navigate('/auth');
    }
  }, [currentUser, authLoading, navigate]);

  useEffect(() => {
    if (currentUser) {
      fetchUserGoalGraphs();
    }
  }, [currentUser]);

  const fetchUserGoalGraphs = async () => {
    if (!currentUser) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const graphs = await apiService.getUserGoalGraphs(currentUser.uid);
      setSavedGraphs(graphs);
      
      if (graphs.length > 0 && !selectedGraph) {
        setSelectedGraph(graphs[0]);
      }
    } catch (err) {
      console.error('Error fetching goal graphs:', err);
      setError('Failed to load your saved goal graphs.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/auth');
  };

  const handleSelectGraph = (graph: SavedGoalGraph) => {
    setSelectedGraph(graph);
  };

  if (authLoading) {
    return (
      <div className="loading-page">
        <div className="spinner"></div>
        <p>Loading user profile...</p>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="container">
        <div className="profile-header">
          <h1>My Profile</h1>
          {currentUser && (
            <div className="user-info">
              <p>Email: {currentUser.email}</p>
              <button className="btn btn-secondary" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>

        <div className="saved-goals-section">
          <h2>My Saved Goals</h2>
          
          {isLoading ? (
            <div className="loading-indicator">
              <div className="spinner"></div>
              <p>Loading your goal graphs...</p>
            </div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : savedGraphs.length === 0 ? (
            <div className="no-data-message">
              <p>You don't have any saved goal graphs yet.</p>
              <button 
                className="btn btn-primary" 
                onClick={() => navigate('/')}
              >
                Create your first goal graph
              </button>
            </div>
          ) : (
            <div className="goal-graphs-container">
              <div className="goal-list">
                <h3>Your Goals</h3>
                <ul>
                  {savedGraphs.map((graph) => (
                    <li 
                      key={graph.id}
                      className={selectedGraph?.id === graph.id ? 'selected' : ''}
                      onClick={() => handleSelectGraph(graph)}
                    >
                      <span className="goal-title">{graph.goal}</span>
                      <span className="goal-date">
                        {new Date(graph.created_at.seconds * 1000).toLocaleDateString()}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="selected-graph">
                {selectedGraph && (
                  <>
                    <h3>{selectedGraph.goal}</h3>
                    <GoalGraph nodes={selectedGraph.nodes} />
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage; 