#!/bin/bash

echo "🛡️  Starting Guardian Angel AI Demo System"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the Guardian_Angel_AI directory"
    exit 1
fi

# Function to check if port is in use
check_port() {
    lsof -i:$1 > /dev/null 2>&1
    return $?
}

# Check if ports are available
if check_port 5000; then
    echo "⚠️  Port 5000 is already in use (Backend)"
    echo "   Kill the process or use a different port"
fi

if check_port 5173; then
    echo "⚠️  Port 5173 is already in use (Frontend)"
    echo "   Kill the process or use a different port"
fi

echo ""
echo "📦 Step 1: Setting up Backend..."
echo "--------------------------------"

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Add your ANTHROPIC_API_KEY to backend/.env for AI summaries (optional)"
fi

# Start backend in background
echo "🚀 Starting Flask backend on http://localhost:5000"
python app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

cd ..

echo ""
echo "🎨 Step 2: Setting up Frontend..."
echo "--------------------------------"

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
else
    echo "npm dependencies already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

# Start frontend in background
echo "🚀 Starting Vite dev server on http://localhost:5173"
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

cd ..

# Save PIDs for later cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo ""
echo "✅ Guardian Angel AI is starting up!"
echo "=========================================="
echo ""
echo "📱 Dashboard:  http://localhost:5173"
echo "🔌 API:        http://localhost:5000"
echo ""
echo "📊 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop: ./stop.sh"
echo ""
echo "⏳ Waiting for services to start..."

sleep 3

# Check if services are running
if check_port 5000; then
    echo "✓ Backend is running"
else
    echo "✗ Backend failed to start (check backend.log)"
fi

if check_port 5173; then
    echo "✓ Frontend is running"
else
    echo "✗ Frontend failed to start (check frontend.log)"
fi

echo ""
echo "🎉 Ready for demo! Open http://localhost:5173 in your browser"
