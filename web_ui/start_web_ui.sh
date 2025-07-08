#!/bin/bash

# MCP Document Exchange Web UI Startup Script
# This script starts the web interface for the MCP-based document processing system

echo "=== MCP Document Exchange Web UI ==="
echo "Starting modern web interface..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the web_ui directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv ../venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source ../venv/Scripts/activate
else
    # Linux/macOS
    source ../venv/bin/activate
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install MCP SDK and dependencies
echo "Installing MCP SDK..."
pip install mcp

# Check if MCP servers are available
echo "Checking MCP server availability..."
if [ ! -f "../servers/document_verification_server/server.py" ]; then
    echo "Warning: Document verification server not found!"
fi

if [ ! -f "../servers/summarization_server/server.py" ]; then
    echo "Warning: Summarization server not found!"
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo ""
echo "Starting Flask web server..."
echo "Web UI will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python app.py
