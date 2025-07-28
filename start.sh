#!/bin/bash

# Start the backend FastAPI server
echo "Starting backend server..."
cd /app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait a moment for backend to start
sleep 3

# Start the frontend development server (for development)
# In production, you might serve the built files with nginx
echo "Starting frontend server..."
cd /app/frontend
npm start &

# Wait for both processes
wait 