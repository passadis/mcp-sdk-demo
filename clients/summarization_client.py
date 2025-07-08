"""
MCP Client for Text Summarization

Demonstrates how to connect to and use the text summarization MCP server.
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
logger = LogConfig.setup_logging("summarization_client")

# Initialize key manager for client
client_key_manager = KeyManager(
    key_dir=os.path.join(Config.KEYS_BASE_DIR, "summarization_client"),
    entity_name="summarization_client"
)


class SummarizationClient:
    """Client for interacting with the text summarization MCP server."""
    
    def __init__(self):
        self.session: ClientSession = None
        self.server_public_key: str = None
        
    async def connect(self, server_command: list[str]):
        """Connect to the text summarization server."""
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
            
            logger.info("Connected to text summarization server")
            
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
                service_available = response_data.get("service_available", False)
                
                logger.info("Retrieved server public key")
                logger.info(f"Service available: {service_available}")
            else:
                logger.error("No response when getting server public key")
                
        except Exception as e:
            logger.error(f"Failed to get server public key: {e}")
    
    async def check_service_status(self):
        """Check the status of the summarization service."""
        try:
            args = {
                "requester_public_key": client_key_manager.get_public_key_pem()
            }
            
            logger.info("Checking service status")
            
            result = await self.session.call_tool("check_service_status", args)
            
            if result.content:
                response_text = result.content[0].text
                return json.loads(response_text)
            else:
                return {"error": "No response from server"}
                
        except Exception as e:
            logger.error(f"Error checking service status: {e}")
            return {"error": str(e)}
    
    async def summarize_text(self, text: str, access_key: str, encrypted: bool = False):
        """Summarize text using the MCP server."""
        try:
            args = {
                "text": text,
                "access_key": access_key,
                "requester_public_key": client_key_manager.get_public_key_pem(),
                "encrypted": encrypted
            }
            
            logger.info(f"Requesting summarization (encrypted: {encrypted}, access_key: {access_key})")
            
            result = await self.session.call_tool("summarize_text", args)
            
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
            logger.error(f"Error summarizing text: {e}")
            return {"error": str(e)}


async def demo_text_summarization():
    """Demonstrate text summarization functionality."""
    logger.info("Starting text summarization demo")
    
    # Command to start the summarization server
    server_command = [
        "python", 
        os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "servers", 
            "summarization_server", 
            "server.py"
        )
    ]
    
    client = SummarizationClient()
    
    try:
        session = await client.connect(server_command)
        
        print("\n=== Text Summarization Demo ===\n")
        
        # Test 1: Check service status
        print("1. Checking service status:")
        status = await client.check_service_status()
        print(json.dumps(status, indent=2))
        
        print("\n" + "="*50 + "\n")
        
        # Test 2: Summarize text with valid access key
        sample_text = """
        Artificial Intelligence (AI) is a rapidly evolving field that encompasses machine learning, 
        natural language processing, computer vision, and robotics. Modern AI systems can perform 
        tasks that traditionally required human intelligence, such as recognizing images, 
        understanding speech, and making decisions. The integration of AI into various industries 
        has led to significant improvements in efficiency, accuracy, and innovation. However, 
        the development of AI also raises important ethical considerations regarding privacy, 
        job displacement, and the need for responsible AI governance. As we continue to advance 
        AI capabilities, it is crucial to balance technological progress with societal well-being 
        and ensure that AI systems are developed and deployed in ways that benefit humanity.
        """
        
        # Test with valid access keys
        valid_access_keys = ["SECRETKEY123", "SUMMARY_ACCESS_777"]
        
        for access_key in valid_access_keys:
            print(f"2. Summarizing text with access key: {access_key}")
            result = await client.summarize_text(sample_text, access_key, encrypted=False)
            print(json.dumps(result, indent=2))
            print("\n" + "-"*30 + "\n")
        
        # Test 3: Try with invalid access key
        print("3. Testing with invalid access key:")
        result = await client.summarize_text(sample_text, "INVALID_KEY", encrypted=False)
        print(json.dumps(result, indent=2))
        
        print("\n" + "="*50 + "\n")
        
        # Test 4: Demonstrate encrypted communication
        print("4. Testing encrypted communication:")
        print("Summarizing text with encryption...")
        encrypted_result = await client.summarize_text(
            sample_text, 
            "SECRETKEY123", 
            encrypted=True
        )
        print(json.dumps(encrypted_result, indent=2))
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"Error running demo: {e}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(demo_text_summarization())
