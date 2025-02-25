import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';

const Header: React.FC = () => {
  const location = useLocation();
  const { currentUser, isLoading } = useUser();

  const isActive = (path: string) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <header className="header">
      <div className="container">
        <div className="logo">
          <Link to="/">GraphedGoal</Link>
        </div>
        <nav className="main-nav">
          <ul>
            <li className={isActive('/')}>
              <Link to="/">Home</Link>
            </li>
            <li className={isActive('/history')}>
              <Link to="/history">History</Link>
            </li>
            <li className={isActive('/about')}>
              <Link to="/about">About</Link>
            </li>
          </ul>
        </nav>
        <div className="auth-nav">
          {!isLoading && (
            currentUser ? (
              <Link to="/profile" className="profile-link">
                <span className="user-email">{currentUser.email?.split('@')[0]}</span>
                <span className="profile-icon">👤</span>
              </Link>
            ) : (
              <Link to="/auth" className="btn btn-primary">
                Login
              </Link>
            )
          )}
        </div>
      </div>
    </header>
  );
};

export default Header; 