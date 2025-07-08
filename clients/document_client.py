"""
MCP Client for Document Verification

Demonstrates how to connect to and use the document verification MCP server.
"""

import asyncio
import json
import os
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add parent directory to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.crypto_utils import KeyManager, decrypt_mcp_request
from shared.config import Config, LogConfig

# Setup logging
logger = LogConfig.setup_logging("document_client")

# Initialize key manager for client
client_key_manager = KeyManager(
    key_dir=os.path.join(Config.KEYS_BASE_DIR, "document_client"),
    entity_name="document_client"
)


class DocumentClient:
    """Client for interacting with the document verification MCP server."""
    
    def __init__(self):
        self.session: ClientSession = None
        self.server_public_key: str = None
        
    async def connect(self, server_command: list[str]):
        """Connect to the document verification server."""
        # Convert command list to string for MCP SDK
        if isinstance(server_command, list):
            command_str = " ".join(f'"{part}"' if " " in part else part for part in server_command)
        else:
            command_str = server_command
            
        server_params = StdioServerParameters(command=command_str)
        
        async with AsyncExitStack() as stack:
            # Connect to server
            self.session = await stack.enter_async_context(
                stdio_client(server_params)
            )
            
            # Initialize session
            await self.session.initialize()
            
            logger.info("Connected to document verification server")
            
            # Get server's public key
            await self._get_server_public_key()
            
            return self.session
    
    async def _get_server_public_key(self):
        """Retrieve the server's public key for secure communication."""
        try:
            result = await self.session.call_tool(
                "get_server_public_key",
                {}
            )
            
            if result.content:
                response_data = json.loads(result.content[0].text)
                self.server_public_key = response_data.get("server_public_key")
                logger.info("Retrieved server public key")
            else:
                logger.error("No response when getting server public key")
                
        except Exception as e:
            logger.error(f"Failed to get server public key: {e}")
    
    async def verify_document(self, document_id: str, encrypted: bool = False):
        """Verify a document by its ID."""
        try:
            args = {
                "document_id": document_id,
                "requester_public_key": client_key_manager.get_public_key_pem(),
                "encrypted": encrypted
            }
            
            logger.info(f"Verifying document: {document_id} (encrypted: {encrypted})")
            
            result = await self.session.call_tool("verify_document", args)
            
            if result.content:
                response_text = result.content[0].text
                response_data = json.loads(response_text)
                
                # Decrypt if response is encrypted
                if response_data.get("encrypted", False):
                    decrypted_data = decrypt_mcp_request(response_data, client_key_manager)
                    return decrypted_data
                else:
                    return response_data
            else:
                return {"error": "No response from server"}
                
        except Exception as e:
            logger.error(f"Error verifying document {document_id}: {e}")
            return {"error": str(e)}
    
    async def list_documents(self, encrypted: bool = False):
        """List all available documents."""
        try:
            args = {
                "requester_public_key": client_key_manager.get_public_key_pem(),
                "encrypted": encrypted
            }
            
            logger.info(f"Listing documents (encrypted: {encrypted})")
            
            result = await self.session.call_tool("list_documents", args)
            
            if result.content:
                response_text = result.content[0].text
                response_data = json.loads(response_text)
                
                # Decrypt if response is encrypted
                if response_data.get("encrypted", False):
                    decrypted_data = decrypt_mcp_request(response_data, client_key_manager)
                    return decrypted_data
                else:
                    return response_data
            else:
                return {"error": "No response from server"}
                
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return {"error": str(e)}


async def demo_document_verification():
    """Demonstrate document verification functionality."""
    logger.info("Starting document verification demo")
    
    # Command to start the document verification server
    # In a real scenario, this would be configured differently
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
    
    try:
        session = await client.connect(server_command)
        
        print("\n=== Document Verification Demo ===\n")
        
        # Test 1: List all documents
        print("1. Listing all available documents:")
        documents = await client.list_documents(encrypted=False)
        print(json.dumps(documents, indent=2))
        
        print("\n" + "="*50 + "\n")
        
        # Test 2: Verify specific documents
        test_documents = ["DOC001", "DOC002", "DOC003", "INVALID_DOC"]
        
        for doc_id in test_documents:
            print(f"2. Verifying document: {doc_id}")
            result = await client.verify_document(doc_id, encrypted=False)
            print(json.dumps(result, indent=2))
            print("\n" + "-"*30 + "\n")
        
        # Test 3: Demonstrate encrypted communication
        print("3. Testing encrypted communication:")
        print("Verifying DOC001 with encryption...")
        encrypted_result = await client.verify_document("DOC001", encrypted=True)
        print(json.dumps(encrypted_result, indent=2))
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"Error running demo: {e}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(demo_document_verification())
