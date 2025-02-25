import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GoalForm from '../components/GoalForm';
import GoalGraph from '../components/GoalGraph';
import { apiService } from '../services/api';
import { GoalRequest, SubgoalNode } from '../types';
import { useUser } from '../contexts/UserContext';

const HomePage: React.FC = () => {
  const { currentUser } = useUser();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [nodes, setNodes] = useState<SubgoalNode[]>([]);
  const [goalText, setGoalText] = useState<string>('');
  const [isSaved, setIsSaved] = useState(false);
  const navigate = useNavigate();
  
  const handleSubmit = async (request: GoalRequest) => {
    setIsLoading(true);
    setError(null);
    setGoalText(request.goal);
    setIsSaved(false);
    
    try {
      // Add user_id to request if user is logged in
      if (currentUser) {
        request.user_id = currentUser.uid;
      }
      
      const response = await apiService.processGoal(request);
      setNodes(response.nodes);
      setIsSaved(response.saved);
    } catch (err) {
      console.error('Error processing goal:', err);
      setError('Failed to process your goal. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewSaved = () => {
    navigate('/profile');
  };

  const handleLogin = () => {
    navigate('/auth');
  };

  return (
    <div className="home-page">
      <div className="container">
        <div className="hero-section">
          <h1>Visualize Your Path to Success</h1>
          <p>
            GraphedGoal helps you break down complex goals into manageable steps
            using AI-powered visualization.
          </p>
        </div>

        <div className="content-section">
          <div className="form-section">
            <GoalForm onSubmit={handleSubmit} isLoading={isLoading} />
            
            {nodes.length > 0 && !currentUser && (
              <div className="login-prompt">
                <p>Login to save your goal graphs and access them later.</p>
                <button onClick={handleLogin} className="btn btn-secondary">
                  Login / Register
                </button>
              </div>
            )}
          </div>

          {isLoading && (
            <div className="loading-section">
              <p>Processing your goal...</p>
              <div className="spinner"></div>
            </div>
          )}

          {error && (
            <div className="error-section">
              <p>{error}</p>
            </div>
          )}

          {nodes.length > 0 && (
            <div className="result-section">
              <div className="result-header">
                <h2>Your Goal: {goalText}</h2>
                {isSaved && (
                  <div className="saved-indicator">
                    <span className="saved-icon">✓</span>
                    <span>Saved</span>
                    <button 
                      onClick={handleViewSaved} 
                      className="btn btn-text"
                    >
                      View all saved goals
                    </button>
                  </div>
                )}
              </div>
              <GoalGraph nodes={nodes} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage; 