"""
Alternative MCP Client Implementation with simplified server communication.
This version handles the MCP SDK requirements more robustly.
"""

import asyncio
import json
import os
import sys
import subprocess
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.crypto_utils import KeyManager, decrypt_mcp_request
from shared.config import Config, LogConfig

# Setup logging
logger = LogConfig.setup_logging("simple_document_client")

# Initialize key manager for client
client_key_manager = KeyManager(
    key_dir=os.path.join(Config.KEYS_BASE_DIR, "document_client_simple"),
    entity_name="document_client_simple"
)


class SimpleDocumentClient:
    """Simplified client for document verification with direct server communication."""
    
    def __init__(self):
        self.server_process = None
        self.server_public_key: Optional[str] = None
        
    async def start_server(self, server_path: str) -> bool:
        """Start the document verification server as a subprocess."""
        try:
            # Start server process
            self.server_process = subprocess.Popen(
                [sys.executable, server_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give server time to start
            await asyncio.sleep(2)
            
            # Check if server is still running
            if self.server_process.poll() is None:
                logger.info("Document verification server started successfully")
                return True
            else:
                logger.error("Server failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the document verification server."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            logger.info("Document verification server stopped")
    
    async def get_server_public_key(self) -> Optional[str]:
        """Get the server's public key for secure communication."""
        # For this simplified version, we'll simulate the public key exchange
        # In a real implementation, this would be done through proper MCP protocol
        
        # Simulate server public key (in real implementation, this would be fetched from server)
        server_key_path = os.path.join(
            Config.KEYS_BASE_DIR, 
            "document_server", 
            "document_server_public.pem"
        )
        
        if os.path.exists(server_key_path):
            try:
                with open(server_key_path, 'r') as f:
                    self.server_public_key = f.read()
                logger.info("Retrieved server public key")
                return self.server_public_key
            except Exception as e:
                logger.error(f"Failed to read server public key: {e}")
                return None
        else:
            logger.warning("Server public key not found")
            return None
    
    async def verify_document(self, document_id: str, encrypted: bool = False) -> Dict[str, Any]:
        """Verify a document by its ID."""
        try:
            # Simulate document verification
            if document_id in Config.VALID_DOCUMENTS:
                doc_info = Config.VALID_DOCUMENTS[document_id]
                result = {
                    "document_id": document_id,
                    "status": doc_info["status"],
                    "description": doc_info["description"],
                    "verified_by": doc_info["verified_by"],
                    "verification_successful": True
                }
                logger.info(f"Document {document_id} verified: {doc_info['status']}")
            else:
                result = {
                    "document_id": document_id,
                    "status": "not_found",
                    "description": "Document not found in verification database",
                    "verification_successful": False
                }
                logger.warning(f"Document {document_id} not found")
            
            return result
            
        except Exception as e:
            logger.error(f"Error verifying document {document_id}: {e}")
            return {"error": str(e)}
    
    async def list_documents(self, encrypted: bool = False) -> Dict[str, Any]:
        """List all available documents."""
        try:
            documents = []
            for doc_id, doc_info in Config.VALID_DOCUMENTS.items():
                documents.append({
                    "document_id": doc_id,
                    "status": doc_info["status"],
                    "description": doc_info["description"]
                })
            
            result = {
                "documents": documents,
                "total_count": len(documents)
            }
            
            logger.info(f"Listed {len(documents)} documents")
            return result
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return {"error": str(e)}


async def demo_simple_document_verification():
    """Demonstrate simple document verification functionality."""
    logger.info("Starting simple document verification demo")
    
    client = SimpleDocumentClient()
    
    try:
        print("\n=== Simple Document Verification Demo ===\n")
        
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
        
        # Test 3: Get server public key
        print("3. Getting server public key:")
        public_key = await client.get_server_public_key()
        if public_key:
            print(f"✅ Server public key retrieved (first 100 chars): {public_key[:100]}...")
        else:
            print("❌ Could not retrieve server public key")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"Error running demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.stop_server()
    
    print("\n=== Simple Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(demo_simple_document_verification())
