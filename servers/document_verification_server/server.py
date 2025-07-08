"""
Document Verification MCP Server

Provides tools for document verification and status checking.
Maintains secure communication through hybrid encryption.
"""

import asyncio
import json
import os
from typing import Any, Sequence

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

# Add parent directory to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.crypto_utils import KeyManager, create_encrypted_response, decrypt_mcp_request
from shared.config import Config, LogConfig

# Setup logging
logger = LogConfig.setup_logging("document_verification_server")

# Initialize key manager
key_manager = KeyManager(
    key_dir=os.path.join(Config.KEYS_BASE_DIR, "document_server"),
    entity_name="document_server"
)

# Create MCP server
server = Server("document-verification-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for document verification."""
    return [
        types.Tool(
            name="verify_document",
            description="Verify the status and authenticity of a document by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "The unique identifier of the document to verify"
                    },
                    "requester_public_key": {
                        "type": "string",
                        "description": "PEM-encoded public key of the requesting entity"
                    },
                    "encrypted": {
                        "type": "boolean",
                        "description": "Whether to return encrypted response",
                        "default": False
                    }
                },
                "required": ["document_id", "requester_public_key"]
            }
        ),
        types.Tool(
            name="list_documents",
            description="List all available documents and their verification status",
            inputSchema={
                "type": "object",
                "properties": {
                    "requester_public_key": {
                        "type": "string",
                        "description": "PEM-encoded public key of the requesting entity"
                    },
                    "encrypted": {
                        "type": "boolean",
                        "description": "Whether to return encrypted response",
                        "default": False
                    }
                },
                "required": ["requester_public_key"]
            }
        ),
        types.Tool(
            name="get_server_public_key",
            description="Get the server's public key for establishing secure communication",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle tool calls for document verification."""
    
    try:
        if name == "get_server_public_key":
            # Return server's public key (unencrypted)
            result = {
                "server_public_key": key_manager.get_public_key_pem(),
                "server_id": "document_verification_server"
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "verify_document":
            document_id = arguments.get("document_id")
            requester_public_key = arguments.get("requester_public_key")
            encrypt_response = arguments.get("encrypted", False)
            
            if not document_id or not requester_public_key:
                raise ValueError("Missing required arguments: document_id or requester_public_key")
            
            logger.info(f"Document verification request for: {document_id}")
            
            # Check if document exists
            if document_id in Config.VALID_DOCUMENTS:
                doc_info = Config.VALID_DOCUMENTS[document_id]
                result = {
                    "document_id": document_id,
                    "status": doc_info["status"],
                    "description": doc_info["description"],
                    "verified_by": doc_info["verified_by"],
                    "verification_successful": True
                }
                logger.info(f"Document {document_id} found: {doc_info['status']}")
            else:
                result = {
                    "document_id": document_id,
                    "status": "not_found",
                    "description": "Document not found in verification database",
                    "verification_successful": False
                }
                logger.warning(f"Document {document_id} not found")
            
            # Encrypt response if requested
            if encrypt_response:
                encrypted_result = create_encrypted_response(
                    result, 
                    requester_public_key, 
                    key_manager
                )
                response_text = json.dumps(encrypted_result, indent=2)
            else:
                response_text = json.dumps(result, indent=2)
            
            return [types.TextContent(
                type="text",
                text=response_text
            )]
            
        elif name == "list_documents":
            requester_public_key = arguments.get("requester_public_key")
            encrypt_response = arguments.get("encrypted", False)
            
            if not requester_public_key:
                raise ValueError("Missing required argument: requester_public_key")
            
            logger.info("Document list request received")
            
            # Prepare document list
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
            
            # Encrypt response if requested
            if encrypt_response:
                encrypted_result = create_encrypted_response(
                    result,
                    requester_public_key,
                    key_manager
                )
                response_text = json.dumps(encrypted_result, indent=2)
            else:
                response_text = json.dumps(result, indent=2)
            
            return [types.TextContent(
                type="text",
                text=response_text
            )]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error handling tool {name}: {e}")
        error_result = {
            "error": str(e),
            "tool": name,
            "success": False
        }
        
        return [types.TextContent(
            type="text",
            text=json.dumps(error_result, indent=2)
        )]


async def main():
    """Run the document verification MCP server."""
    logger.info("Starting Document Verification MCP Server")
    logger.info(f"Server public key: {key_manager.get_public_key_pem()[:100]}...")
    logger.info(f"Available documents: {list(Config.VALID_DOCUMENTS.keys())}")
    
    # Initialize server options
    init_options = InitializationOptions(
        server_name="document-verification-server",
        server_version="1.0.0"
    )
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            init_options
        )


if __name__ == "__main__":
    asyncio.run(main())
