import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import GoalForm from './GoalForm';

describe('GoalForm', () => {
  const mockSubmit = jest.fn();
  
  beforeEach(() => {
    mockSubmit.mockClear();
  });
  
  it('renders correctly', () => {
    render(<GoalForm onSubmit={mockSubmit} isLoading={false} />);
    
    expect(screen.getByPlaceholderText(/Enter your goal/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Visualize My Goal/i })).toBeInTheDocument();
  });
  
  it('shows loading state when isLoading is true', () => {
    render(<GoalForm onSubmit={mockSubmit} isLoading={true} />);
    
    expect(screen.getByRole('button', { name: /Processing/i })).toBeDisabled();
  });
  
  it('submits the form with the entered goal', () => {
    render(<GoalForm onSubmit={mockSubmit} isLoading={false} />);
    
    // Enter a goal
    const input = screen.getByPlaceholderText(/Enter your goal/i);
    fireEvent.change(input, { target: { value: 'Learn to play guitar' } });
    
    // Submit the form
    const button = screen.getByRole('button', { name: /Visualize My Goal/i });
    fireEvent.click(button);
    
    // Check that onSubmit was called with the correct goal
    expect(mockSubmit).toHaveBeenCalledWith({ goal: 'Learn to play guitar' });
  });
  
  it('validates that goal is not empty', () => {
    render(<GoalForm onSubmit={mockSubmit} isLoading={false} />);
    
    // Try to submit with empty goal
    const button = screen.getByRole('button', { name: /Visualize My Goal/i });
    fireEvent.click(button);
    
    // onSubmit should not be called
    expect(mockSubmit).not.toHaveBeenCalled();
    
    // Check for validation error
    expect(screen.getByText(/Please enter your goal/i)).toBeInTheDocument();
  });
}); 