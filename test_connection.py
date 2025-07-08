#!/usr/bin/env python3
"""
Simple test script to verify MCP client connections work properly.
"""

import asyncio
import os
import sys
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.document_client import DocumentClient
from shared.config import LogConfig

logger = LogConfig.setup_logging("connection_test")

async def test_document_client():
    """Test basic document client connection."""
    print("Testing Document Client Connection...")
    
    try:
        # Simple server command
        server_command = [
            "python", 
            os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "servers", 
                "document_verification_server", 
                "server.py"
            )
        ]
        
        client = DocumentClient()
        
        # Test connection
        session = await client.connect(server_command)
        
        print("✅ Successfully connected to document verification server")
        
        # Test a simple operation
        result = await client.list_documents(encrypted=False)
        print(f"✅ Successfully retrieved documents: {len(result.get('documents', []))} found")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run connection tests."""
    print("="*50)
    print("MCP Client Connection Test")
    print("="*50)
    
    success = await test_document_client()
    
    if success:
        print("\n✅ All tests passed! MCP client is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
    
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
