@echo off
REM MCP Document Exchange Web UI Startup Script (Windows)
REM This script starts the web interface for the MCP-based document processing system

echo === MCP Document Exchange Web UI ===
echo Starting modern web interface...

REM Check if we're in the right directory
if not exist "app.py" (
    echo Error: app.py not found. Please run this script from the web_ui directory.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "..\venv" (
    echo Creating Python virtual environment...
    python -m venv ..\venv
)

REM Activate virtual environment
echo Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Install MCP SDK and dependencies
echo Installing MCP SDK...
pip install mcp

REM Check if MCP servers are available
echo Checking MCP server availability...
if not exist "..\servers\document_verification_server\server.py" (
    echo Warning: Document verification server not found!
)

if not exist "..\servers\summarization_server\server.py" (
    echo Warning: Summarization server not found!
)

REM Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo.
echo Starting Flask web server...
echo Web UI will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause
