# Contributing to GraphedGoal

Thank you for considering contributing to GraphedGoal! This document provides guidelines and instructions for contributing to this project.

## Development Setup

### Prerequisites
- Node.js and Yarn for frontend development
- Python 3.8+ for backend development
- OpenAI API key
- Firebase project and service account key

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with your OpenAI API key and Firebase configuration (see `.env.sample` for reference).

6. Run the backend server:
   ```
   python main.py
   ```
   or
   ```
   ./run.sh
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   yarn install
   ```

3. Create a `.env` file in the frontend directory with your API URL and Firebase configuration (see `.env.sample` for reference).

4. Start the development server:
   ```
   yarn start
   ```

## Testing

### Backend Tests
To run backend tests:
```
cd backend
pytest
```

### Frontend Tests
To run frontend tests:
```
cd frontend
yarn test
```

## Debugging

The project includes VSCode debug configurations for both frontend and backend:

1. **Python: FastAPI** - Launches the FastAPI backend server
2. **React: Frontend** - Launches Chrome and connects to the React frontend
3. **Python: Run Tests** - Runs the backend tests with the debugger
4. **Full Stack** - Launches both backend and frontend simultaneously

To use these configurations, open the Debug panel in VSCode and select the appropriate configuration.

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- For Python code, follow PEP 8 guidelines
- For React/TypeScript, follow the ESLint configuration in the project

## Git Hooks

The project uses Husky to run pre-commit hooks that ensure tests pass before committing. To set up Husky:

```
./setup-husky.sh
```

## Project Structure

### Backend
- `backend/main.py` - FastAPI application entry point
- `backend/firebase_config.py` - Firebase integration
- `backend/tests/` - Backend tests
- `backend/requirements.txt` - Python dependencies

### Frontend
- `frontend/src/` - React application source code
- `frontend/src/components/` - Reusable React components
- `frontend/src/pages/` - Page components
- `frontend/src/services/` - API service classes
- `frontend/src/utils/` - Utility functions
- `frontend/src/contexts/` - React context providers
- `frontend/src/types/` - TypeScript type definitions

## License

This project is licensed under the MIT License - see the LICENSE file for details. 