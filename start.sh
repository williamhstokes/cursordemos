#!/bin/bash

# NFL Dashboard Startup Script
echo "🏈 Starting NFL Dashboard Server..."
echo "=================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 to run the server."
    exit 1
fi

# Check if required files exist
if [ ! -f "nfl_logos.json" ]; then
    echo "❌ nfl_logos.json not found. Please ensure all files are in the correct location."
    exit 1
fi

if [ ! -f "server.py" ]; then
    echo "❌ server.py not found. Please ensure all files are in the correct location."
    exit 1
fi

# Start the server
echo "🚀 Launching server on http://localhost:8000"
echo "📊 Dashboard will be available at: http://localhost:8000"
echo "🔧 API endpoints available at: http://localhost:8000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

python3 server.py