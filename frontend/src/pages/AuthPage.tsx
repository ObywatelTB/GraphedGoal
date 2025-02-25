import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../components/Auth/LoginForm';
import RegisterForm from '../components/Auth/RegisterForm';

enum AuthMode {
  LOGIN = 'login',
  REGISTER = 'register',
}

const AuthPage: React.FC = () => {
  const [mode, setMode] = useState<AuthMode>(AuthMode.LOGIN);
  const navigate = useNavigate();

  const handleAuthSuccess = () => {
    navigate('/');
  };

  const toggleMode = () => {
    setMode(mode === AuthMode.LOGIN ? AuthMode.REGISTER : AuthMode.LOGIN);
  };

  return (
    <div className="auth-page">
      <div className="container">
        <div className="auth-container">
          <div className="auth-card">
            {mode === AuthMode.LOGIN ? (
              <LoginForm 
                onSuccess={handleAuthSuccess} 
                onRegisterClick={toggleMode} 
              />
            ) : (
              <RegisterForm 
                onSuccess={handleAuthSuccess} 
                onLoginClick={toggleMode} 
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage; 