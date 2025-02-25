import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get host and port from environment variables or use defaults
host = os.getenv("BACKEND_HOST", "0.0.0.0")
port = int(os.getenv("BACKEND_PORT", "8000"))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=True) 