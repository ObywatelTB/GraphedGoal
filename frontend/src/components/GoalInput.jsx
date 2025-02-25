import React, { useState } from 'react';
import axios from 'axios';
import './GoalInput.css';

const GoalInput = ({ onGoalProcessed }) => {
  const [goal, setGoal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!goal.trim()) {
      setError('Please enter a goal');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Get API URL from environment variable or use default
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      
      const response = await axios.post(`${apiUrl}/api/v1/goals/process`, {
        goal: goal,
        // We'll add user_id when authentication is implemented
        user_id: null
      });
      
      // Pass the processed goal data to the parent component
      if (onGoalProcessed) {
        onGoalProcessed(response.data);
      }
      
      // Clear the input field after successful submission
      setGoal('');
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while processing your goal');
      console.error('Error processing goal:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="goal-input-container">
      <h1>GraphedGoal</h1>
      <p className="subtitle">Visualize the path to achieve your personal goals</p>
      
      <form onSubmit={handleSubmit} className="goal-form">
        <div className="form-group">
          <label htmlFor="goal-input">What's your goal?</label>
          <textarea
            id="goal-input"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="Enter your goal here (e.g., 'Learn to play the piano', 'Start a successful online business')"
            rows={4}
            disabled={isLoading}
          />
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button 
          type="submit" 
          className="submit-button"
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Visualize My Goal'}
        </button>
      </form>
    </div>
  );
};

export default GoalInput; 