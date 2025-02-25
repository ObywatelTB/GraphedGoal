import React, { useState } from 'react';
import GoalForm from '../components/GoalForm';
import GoalGraph from '../components/GoalGraph';
import { apiService } from '../services/api';
import { GoalRequest, SubgoalNode } from '../types';

const HomePage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [nodes, setNodes] = useState<SubgoalNode[]>([]);
  const [goalText, setGoalText] = useState<string>('');

  const handleSubmit = async (request: GoalRequest) => {
    setIsLoading(true);
    setError(null);
    setGoalText(request.goal);
    
    try {
      const response = await apiService.processGoal(request);
      setNodes(response.nodes);
    } catch (err) {
      console.error('Error processing goal:', err);
      setError('Failed to process your goal. Please try again.');
    } finally {
      setIsLoading(false);
    }
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
              <h2>Your Goal: {goalText}</h2>
              <GoalGraph nodes={nodes} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage; 