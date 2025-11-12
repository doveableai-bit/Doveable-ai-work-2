#!/bin/bash
# Start backend on port 8000
python3 main.py &
# Wait a moment for backend to start
sleep 2
# Start frontend on port 5000
npm run dev
