import React from 'react';

const AboutPage: React.FC = () => {
  return (
    <div className="about-page">
      <div className="container">
        <h1>About GraphedGoal</h1>
        
        <section className="about-section">
          <h2>Our Mission</h2>
          <p>
            GraphedGoal was created to help people visualize and break down their complex goals into manageable steps.
            We believe that proper goal planning is essential for success, and visualization can make the process more intuitive and effective.
          </p>
        </section>
        
        <section className="about-section">
          <h2>How It Works</h2>
          <p>
            GraphedGoal uses OpenAI's o3-mini language model to analyze your goal and break it down into a hierarchical structure of subgoals and steps.
            The result is presented as an interactive graph visualization that you can explore to understand the path to achieving your goal.
          </p>
          
          <div className="steps">
            <div className="step">
              <h3>1. Enter Your Goal</h3>
              <p>Start by describing your goal in detail. The more specific you are, the better the breakdown will be.</p>
            </div>
            
            <div className="step">
              <h3>2. AI Processing</h3>
              <p>Our AI analyzes your goal and identifies the key components and steps needed to achieve it.</p>
            </div>
            
            <div className="step">
              <h3>3. Visualization</h3>
              <p>Explore the interactive graph to see how your goal breaks down into manageable subgoals and steps.</p>
            </div>
          </div>
        </section>
        
        <section className="about-section">
          <h2>Technology</h2>
          <p>
            GraphedGoal is built using modern web technologies:
          </p>
          <ul>
            <li>React for the frontend user interface</li>
            <li>FastAPI for the backend API</li>
            <li>OpenAI's o3-mini language model for goal analysis</li>
            <li>Force-directed graph visualization for an interactive experience</li>
            <li>Firebase for data storage and user management</li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default AboutPage; 