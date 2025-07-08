@echo off
REM Setup script for MCP SDK Implementation (Windows)

echo Setting up MCP SDK Implementation...

REM Create virtual environment
echo Creating virtual environment...
python -m venv mcp_env

REM Activate virtual environment
echo Activating virtual environment...
call mcp_env\Scripts\activate

REM Install requirements
echo Installing Python packages...
pip install -r requirements.txt

REM Create keys directory
echo Creating keys directory...
mkdir keys\document_server 2>nul
mkdir keys\summarization_server 2>nul
mkdir keys\document_client 2>nul
mkdir keys\summarization_client 2>nul

REM Copy environment template
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template. Please update with your Azure OpenAI credentials.
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Update .env file with your Azure OpenAI credentials
echo 2. Activate the virtual environment:
echo    call mcp_env\Scripts\activate
echo 3. Start the servers:
echo    python servers\document_verification_server\server.py
echo    python servers\summarization_server\server.py
echo 4. Run the clients:
echo    python clients\document_client.py
echo    python clients\summarization_client.py

pause
