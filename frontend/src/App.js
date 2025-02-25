import React, { useState } from 'react';
import GoalInput from './components/GoalInput';
import './App.css';

function App() {
  const [goalData, setGoalData] = useState(null);
  
  const handleGoalProcessed = (data) => {
    setGoalData(data);
    // We'll add graph visualization here later
  };
  
  return (
    <div className="app">
      {!goalData ? (
        <GoalInput onGoalProcessed={handleGoalProcessed} />
      ) : (
        <div className="results-container">
          <h2>Your Goal Plan</h2>
          <p>We'll implement the graph visualization here</p>
          
          {/* Temporary display of the nodes as a list */}
          <div className="nodes-list">
            <h3>Subgoals and Steps:</h3>
            <ul>
              {goalData.nodes.map(node => (
                <li key={node.id}>
                  <strong>{node.label}</strong>
                  {node.description && <p>{node.description}</p>}
                </li>
              ))}
            </ul>
          </div>
          
          <button 
            className="back-button"
            onClick={() => setGoalData(null)}
          >
            Create Another Goal
          </button>
        </div>
      )}
    </div>
  );
}

export default App; 