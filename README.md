# GraphedGoal

<!-- Komentarz -->

A web application that helps users visualize paths to achieve their personal goals.

## Concept

GraphedGoal allows users to input a goal they want to achieve, then processes it using OpenAI's o3-mini LLM to generate 5-15 subgoals and steps in the form of a tree-graph. This visual representation helps users break down complex goals into manageable steps.

## Technologies

### System
- macOS

### Frontend
- React (installed with yarn)
- Beautiful, minimalistic UI with Lato font

### Backend
- Python FastAPI
- Virtual environment for dependency management
- Modular structure with services, models, and API layers

### Database
- Firebase
- Configured with Google Cloud CLI

### Version Control
- Git repository on GitHub (ObywatelTB)

## Tasks

### To Do
- [x] Create README with concept, tasks, and technologies
- [x] Create GitHub repository
- [x] Set up basic backend with FastAPI
- [x] Set up basic frontend with React
- [x] Connect with existing Firebase database - set the keys in .env
- [x] Implement LLM processing with OpenAI o3-mini
- [x] Implement tree-graph visualization
- [x] Set up unit tests for frontend and backend
- [x] Create pre-commit hook for running tests
- [x] Configure launch for breakpoint debugging
- [x] Create comprehensive documentation
- [x] Refactor backend for better modularity

## Repository
The project is hosted on GitHub: [GraphedGoal](https://github.com/ObywatelTB/GraphedGoal)

## Getting Started

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

### Backend Architecture
The backend follows a modular architecture:
- `app/main.py`: Application entry point and configuration
- `app/api/`: API endpoints and routing
- `app/models/`: Data models using Pydantic
- `app/services/`: Business logic and external service integration
- `app/db/`: Database connections and operations
- `app/core/`: Core functionality and configuration

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

## Environment Variables

The following environment variables are needed:
- OPENAI_API_KEY - Your OpenAI API key
- FIREBASE_SERVICE_ACCOUNT_KEY - Path to your Firebase service account key JSON file
- BACKEND_HOST - Host for the backend server (default: 0.0.0.0)
- BACKEND_PORT - Port for the backend server (default: 8000)
- REACT_APP_API_URL - URL for the backend API (default: http://localhost:8000)
- Firebase configuration variables for the frontend (see `.env.sample`)

*Detailed setup instructions will be provided as the project progresses.* 

## Testing

### Backend Tests
The backend uses pytest for unit testing. To run the tests:
```
cd backend
pytest
```

### Frontend Tests
The frontend uses Jest and React Testing Library for unit testing. To run the tests:
```
cd frontend
yarn test
```

## Debugging

The project includes VSCode debug configurations for both frontend and backend development. These can be accessed from the Debug panel in VSCode.

## Contributing

For detailed information on how to contribute to this project, see [CONTRIBUTING.md](CONTRIBUTING.md). 
