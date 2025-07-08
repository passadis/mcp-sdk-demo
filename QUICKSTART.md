# Quick Start Guide - MCP SDK Implementation

Get up and running with the MCP SDK implementation in 5 minutes.

## Prerequisites

- Python 3.8+
- Azure OpenAI account (for summarization features)

## Step 1: Setup

### Windows:
```bash
cd mcp_sdk_implementation
./setup.bat
```

### Linux/Mac:
```bash
cd mcp_sdk_implementation
chmod +x setup.sh
./setup.sh
```

## Step 2: Configure Azure OpenAI (Optional)

Edit `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

> **Note:** Document verification works without Azure OpenAI. Only summarization requires it.

## Step 3: Run the Demo

Activate the virtual environment:
```bash
# Windows
call mcp_env\Scripts\activate

# Linux/Mac  
source mcp_env/bin/activate
```

Run the integration demo:
```bash
python integration_demo.py
```

## What You'll See

The demo will show:

1. **🔗 Server Connection**: MCP clients connecting to servers
2. **📋 Document Discovery**: Listing available documents  
3. **🔐 Document Verification**: Verifying documents with encryption
4. **📝 Text Summarization**: AI-powered text summarization
5. **🔒 End-to-End Encryption**: Secure workflows

## Example Output

```
🔗 Connecting to MCP servers...
✅ Connected to both MCP servers

📋 Scenario 1: Document Discovery and Verification
--------------------------------------------------
🔍 Discovering available documents...
Found 3 documents:
  ✅ DOC001: Contract Agreement 2024 (verified)
  ✅ DOC002: Financial Report Q4 (verified)  
  ❌ DOC003: Outdated Policy Document (revoked)

🔐 Verifying document: DOC001
✅ Document verified: verified
   Description: Contract Agreement 2024
```

## Individual Components

### Run Document Server Only
```bash
python servers/document_verification_server/server.py
```

### Run Summarization Server Only  
```bash
python servers/summarization_server/server.py
```

### Test Document Client
```bash
python clients/document_client.py
```

### Test Summarization Client
```bash
python clients/summarization_client.py
```

## Testing the Implementation

Run the test suite:
```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

## Key Features Demonstrated

- ✅ **MCP Protocol**: Standard Model Context Protocol implementation
- ✅ **Tool Discovery**: Automatic API discovery and schema validation
- ✅ **Hybrid Encryption**: RSA + AES-GCM for secure communication
- ✅ **Access Control**: Key-based authorization for services
- ✅ **Azure OpenAI Integration**: AI-powered text summarization
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Multi-Server Architecture**: Distributed service architecture

## Troubleshooting

### Common Issues

1. **"mcp module not found"**
   ```bash
   pip install mcp
   ```

2. **Azure OpenAI errors**
   - Check your `.env` configuration
   - Verify your Azure OpenAI deployment is active
   - Document verification will work without Azure OpenAI

3. **Permission errors on Windows**
   ```bash
   # Run as administrator or use:
   python -m venv mcp_env --system-site-packages
   ```

### Getting Help

- Check the logs for detailed error messages
- Review `MIGRATION_GUIDE.md` for implementation details
- Compare with the original implementation in parent directories

## Next Steps

1. **Explore the Code**: Review the server and client implementations
2. **Customize**: Modify the tools and add your own functionality  
3. **Deploy**: Adapt for your production environment
4. **Integrate**: Connect with your existing MCP-aware applications

## Architecture Overview

```
MCP Clients          MCP Servers
┌─────────────┐     ┌──────────────────┐
│ Document    │────►│ Document         │
│ Client      │     │ Verification     │
└─────────────┘     │ Server           │
                    └──────────────────┘
┌─────────────┐     ┌──────────────────┐
│ Summary     │────►│ Text             │
│ Client      │     │ Summarization    │
└─────────────┘     │ Server           │
                    └──────────────────┘
```

Each component is independent and can be developed, tested, and deployed separately while maintaining secure communication through the MCP protocol.
