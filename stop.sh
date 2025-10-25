#!/bin/bash

echo "🛑 Stopping Guardian Angel AI..."
echo ""

# Kill backend
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
    fi
    rm .backend.pid
fi

# Kill frontend
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
    fi
    rm .frontend.pid
fi

# Fallback: kill by port
echo "Checking for any remaining processes..."

# Kill process on port 5000 (Backend)
PORT_5000_PID=$(lsof -ti:5000)
if [ ! -z "$PORT_5000_PID" ]; then
    echo "Killing process on port 5000..."
    kill $PORT_5000_PID 2>/dev/null
fi

# Kill process on port 5173 (Frontend)
PORT_5173_PID=$(lsof -ti:5173)
if [ ! -z "$PORT_5173_PID" ]; then
    echo "Killing process on port 5173..."
    kill $PORT_5173_PID 2>/dev/null
fi

echo ""
echo "✅ Guardian Angel AI stopped"
