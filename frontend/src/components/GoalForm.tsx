import React, { useState } from 'react';
import { GoalRequest } from '../types';

interface GoalFormProps {
  onSubmit: (request: GoalRequest) => void;
  isLoading: boolean;
}

const GoalForm: React.FC<GoalFormProps> = ({ onSubmit, isLoading }) => {
  const [goal, setGoal] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (goal.trim()) {
      onSubmit({ goal });
    }
  };

  return (
    <div className="goal-form-container">
      <h2>Enter Your Goal</h2>
      <p>
        Describe a personal or professional goal you want to achieve, and we'll help you break it down into manageable steps.
      </p>
      <form onSubmit={handleSubmit} className="goal-form">
        <div className="form-group">
          <textarea
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g., Learn to play the piano, Start a successful online business, Run a marathon..."
            rows={4}
            required
            disabled={isLoading}
          />
        </div>
        <button type="submit" className="submit-button" disabled={isLoading || !goal.trim()}>
          {isLoading ? 'Processing...' : 'Visualize My Goal'}
        </button>
      </form>
    </div>
  );
};

export default GoalForm; 