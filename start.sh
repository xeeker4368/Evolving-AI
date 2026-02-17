#!/bin/bash

# Ultimate AI System v8.0 - Start Script
# FIXED: Uses correct virtual environment path

# Check if running with --debug flag
DEBUG=false
if [ "$1" == "--debug" ]; then
    DEBUG=true
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 2
fi

# Activate virtual environment
# FIX: Use the venv where packages are actually installed
if [ -d "/home/localadmin/venv" ]; then
    source /home/localadmin/venv/bin/activate
    echo "✅ Using /home/localadmin/venv"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Using local venv"
else
    echo "❌ No virtual environment found!"
    echo "Run: python3 -m venv venv"
    exit 1
fi

# Start the application
if [ "$DEBUG" = true ]; then
    echo "🐛 Starting in DEBUG mode..."
    python3 main.py
else
    echo "🚀 Starting Ultimate AI System v8.0..."
    python3 main.py > /dev/null 2>&1 &
    
    # Wait a moment for server to start
    sleep 2
    
    # Save PID
    echo $! > .ai_pid
    
    echo "✅ AI System started!"
    echo "📱 Access: http://localhost:5000"
    echo "🛑 Stop: ./stop.sh"
fi
