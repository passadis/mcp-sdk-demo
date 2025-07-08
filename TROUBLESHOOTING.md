# Troubleshooting Guide - MCP SDK Issues

## Issue: StdioServerParameters command validation error

### Problem
```
1 validation error for StdioServerParameters
command
  Input should be a valid string [type=string_type, input_value=['python', 'path...'], input_type=list]
```

### Root Cause
The MCP SDK expects the `command` parameter to be a string, not a list of strings.

### Solutions

#### Solution 1: Update Client Code (Applied)
The client code has been updated to convert command lists to strings:

```python
# Convert command list to string for MCP SDK
if isinstance(server_command, list):
    command_str = " ".join(f'"{part}"' if " " in part else part for part in server_command)
else:
    command_str = server_command
    
server_params = StdioServerParameters(command=command_str)
```

#### Solution 2: Use Simple Client (Alternative)
A simplified client implementation (`simple_document_client.py`) that bypasses the MCP SDK connection issues.

### Testing the Fix

#### Test 1: Run the connection test
```bash
python test_connection.py
```

#### Test 2: Run the simple client demo
```bash
python clients/simple_document_client.py
```

#### Test 3: Run the integration demo
```bash
python integration_demo.py
```

## Alternative Approaches

### Option 1: Use Different MCP SDK Version
Try downgrading the MCP SDK:
```bash
pip install mcp==0.8.0
```

### Option 2: Use HTTP-based MCP Server
Instead of stdio, use HTTP transport:

```python
from mcp.client.http import http_client

async def connect_http():
    async with http_client("http://localhost:8080") as session:
        await session.initialize()
        return session
```

### Option 3: Direct Server Communication
Use the `SimpleDocumentClient` which communicates directly with the server logic without MCP protocol overhead.

## Environment Setup Issues

### Missing Dependencies
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Python Path Issues
Make sure the shared modules are accessible:
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
```

### Key Generation Issues
Ensure keys directory exists:
```bash
mkdir -p keys/document_server
mkdir -p keys/summarization_server
mkdir -p keys/document_client
mkdir -p keys/summarization_client
```

## Debugging Steps

### Step 1: Check MCP SDK Version
```python
import mcp
print(f"MCP Version: {mcp.__version__}")
```

### Step 2: Test Basic MCP Functionality
```python
from mcp import StdioServerParameters

# Test with string command
params = StdioServerParameters(command="python --version")
print("✅ String command works")

# Test with list command (should fail)
try:
    params = StdioServerParameters(command=["python", "--version"])
    print("❌ List command should not work")
except Exception as e:
    print(f"✅ List command correctly fails: {e}")
```

### Step 3: Test Server Startup
```python
import subprocess
import sys

# Test server startup
server_path = "servers/document_verification_server/server.py"
process = subprocess.Popen([sys.executable, server_path])
print(f"Server process ID: {process.pid}")
process.terminate()
```

## Working Examples

### Example 1: Direct Tool Usage
```python
from shared.config import Config

# Direct document verification
def verify_document_direct(document_id: str):
    if document_id in Config.VALID_DOCUMENTS:
        return Config.VALID_DOCUMENTS[document_id]
    else:
        return {"error": "Document not found"}

# Test
result = verify_document_direct("DOC001")
print(result)
```

### Example 2: Simple Async Client
```python
import asyncio
from clients.simple_document_client import SimpleDocumentClient

async def main():
    client = SimpleDocumentClient()
    result = await client.verify_document("DOC001")
    print(result)

asyncio.run(main())
```

## Next Steps

1. **Test the fixes**: Run the test scripts to verify the fixes work
2. **Use alternatives**: If MCP SDK issues persist, use the simple client
3. **File bug report**: If issues continue, consider filing a bug report with the MCP SDK team
4. **Gradual migration**: Start with the simple client and migrate to full MCP SDK once issues are resolved

## Success Indicators

You'll know the fix works when:
- ✅ `python test_connection.py` runs without errors
- ✅ `python clients/simple_document_client.py` shows document verification results
- ✅ `python integration_demo.py` completes the full workflow
- ✅ No more `StdioServerParameters` validation errors
