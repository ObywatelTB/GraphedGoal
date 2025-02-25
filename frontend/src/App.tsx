import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// Import these components when they're implemented
// import Header from './components/Header';
// import HomePage from './pages/HomePage';
// import AboutPage from './pages/AboutPage';
// import HistoryPage from './pages/HistoryPage';
// import AuthPage from './pages/AuthPage';
// import ProfilePage from './pages/ProfilePage';
// import { UserProvider } from './contexts/UserContext';
import './App.css';

const App: React.FC = () => {
  return (
    // Uncomment UserProvider when implemented
    // <UserProvider>
      <Router>
        <div className="app">
          {/* Add Header when implemented */}
          {/* <Header /> */}
          <main className="main-content">
            <Routes>
              <Route path="/" element={<SimplePlaceholder title="Home Page" />} />
              {/* Add these routes when the components are implemented
              <Route path="/about" element={<AboutPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/auth" element={<AuthPage />} />
              <Route path="/profile" element={<ProfilePage />} /> */}
            </Routes>
          </main>
          <footer className="footer">
            <div className="container">
              <p>&copy; {new Date().getFullYear()} GraphedGoal. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </Router>
    // </UserProvider>
  );
};

// Simple placeholder component for testing
const SimplePlaceholder: React.FC<{ title: string }> = ({ title }) => {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>{title}</h1>
      <p>Welcome to GraphedGoal! The app is currently under development.</p>
    </div>
  );
};

export default App; 