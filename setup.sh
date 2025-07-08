#!/bin/bash

# Setup script for MCP SDK Implementation

echo "Setting up MCP SDK Implementation..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv mcp_env

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source mcp_env/Scripts/activate
else
    source mcp_env/bin/activate
fi

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Create keys directory
echo "Creating keys directory..."
mkdir -p keys/document_server
mkdir -p keys/summarization_server
mkdir -p keys/document_client
mkdir -p keys/summarization_client

# Copy environment template
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please update with your Azure OpenAI credentials."
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your Azure OpenAI credentials"
echo "2. Activate the virtual environment:"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "   source mcp_env/Scripts/activate"
else
    echo "   source mcp_env/bin/activate"
fi
echo "3. Start the servers:"
echo "   python servers/document_verification_server/server.py"
echo "   python servers/summarization_server/server.py"
echo "4. Run the clients:"
echo "   python clients/document_client.py"
echo "   python clients/summarization_client.py"
