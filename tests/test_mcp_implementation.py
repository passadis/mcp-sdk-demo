"""
Test suite for MCP SDK implementation.
"""

import pytest
import asyncio
import json
import tempfile
import os
from unittest.mock import AsyncMock, patch

# Add parent directory to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.crypto_utils import HybridCrypto, KeyManager, create_encrypted_response, decrypt_mcp_request
from shared.config import Config


class TestHybridCrypto:
    """Test hybrid encryption functionality."""
    
    def test_key_generation(self):
        """Test RSA key pair generation."""
        private_key, public_key = HybridCrypto.generate_key_pair()
        
        assert private_key is not None
        assert public_key is not None
        assert private_key.key_size == 2048
    
    def test_encrypt_decrypt_message(self):
        """Test message encryption and decryption."""
        # Generate keys
        private_key, public_key = HybridCrypto.generate_key_pair()
        
        # Test message
        message = "This is a test message for encryption"
        
        # Encrypt
        encrypted_payload = HybridCrypto.encrypt_message(message, public_key)
        assert encrypted_payload is not None
        assert isinstance(encrypted_payload, str)
        
        # Verify it's valid JSON
        payload_dict = json.loads(encrypted_payload)
        assert "encrypted_aes_key" in payload_dict
        assert "nonce" in payload_dict
        assert "ciphertext" in payload_dict
        
        # Decrypt
        decrypted_message = HybridCrypto.decrypt_message(encrypted_payload, private_key)
        assert decrypted_message == message
    
    def test_public_key_pem_conversion(self):
        """Test public key PEM string conversion."""
        private_key, public_key = HybridCrypto.generate_key_pair()
        
        # Convert to PEM string
        pem_string = HybridCrypto.public_key_to_pem_string(public_key)
        assert isinstance(pem_string, str)
        assert "-----BEGIN PUBLIC KEY-----" in pem_string
        assert "-----END PUBLIC KEY-----" in pem_string
        
        # Convert back from PEM string
        recovered_key = HybridCrypto.public_key_from_pem_string(pem_string)
        
        # Test that we can encrypt with recovered key
        message = "Test with recovered key"
        encrypted = HybridCrypto.encrypt_message(message, recovered_key)
        decrypted = HybridCrypto.decrypt_message(encrypted, private_key)
        assert decrypted == message


class TestKeyManager:
    """Test key manager functionality."""
    
    def test_key_manager_creation(self):
        """Test key manager initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            key_manager = KeyManager(temp_dir, "test_entity")
            
            assert key_manager.private_key is not None
            assert key_manager.public_key is not None
            
            # Check files were created
            assert os.path.exists(key_manager.private_key_path)
            assert os.path.exists(key_manager.public_key_path)
    
    def test_key_manager_encrypt_decrypt(self):
        """Test encryption/decryption through key manager."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create two key managers
            alice = KeyManager(temp_dir, "alice")
            bob = KeyManager(temp_dir, "bob")
            
            message = "Hello from Alice to Bob"
            
            # Alice encrypts for Bob
            encrypted = alice.encrypt_for_recipient(message, bob.get_public_key_pem())
            
            # Bob decrypts Alice's message
            decrypted = bob.decrypt_message(encrypted)
            
            assert decrypted == message
    
    def test_key_persistence(self):
        """Test that keys persist across key manager instances."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create first key manager
            km1 = KeyManager(temp_dir, "persistent_test")
            original_public_key = km1.get_public_key_pem()
            
            # Create second key manager with same parameters
            km2 = KeyManager(temp_dir, "persistent_test")
            loaded_public_key = km2.get_public_key_pem()
            
            # Keys should be the same
            assert original_public_key == loaded_public_key


class TestConfig:
    """Test configuration functionality."""
    
    def test_azure_openai_validation(self):
        """Test Azure OpenAI configuration validation."""
        # Mock missing configuration
        with patch.object(Config, 'AZURE_OPENAI_API_KEY', None):
            valid, missing = Config.validate_azure_openai_config()
            assert not valid
            assert "AZURE_OPENAI_KEY" in missing
    
    def test_server_info(self):
        """Test server information retrieval."""
        doc_info = Config.get_server_info("document")
        assert "host" in doc_info
        assert "port" in doc_info
        assert "url" in doc_info
        
        summary_info = Config.get_server_info("summarization")
        assert "host" in summary_info
        assert "port" in summary_info
        assert "url" in summary_info
        
        # Test invalid server type
        with pytest.raises(ValueError):
            Config.get_server_info("invalid_server")


class TestMCPResponseUtils:
    """Test MCP response utility functions."""
    
    def test_create_encrypted_response(self):
        """Test encrypted response creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            sender = KeyManager(temp_dir, "sender")
            recipient = KeyManager(temp_dir, "recipient")
            
            data = {"message": "test data", "status": "success"}
            
            encrypted_response = create_encrypted_response(
                data,
                recipient.get_public_key_pem(),
                sender
            )
            
            assert encrypted_response["encrypted"] is True
            assert "payload" in encrypted_response
            assert "sender_public_key" in encrypted_response
    
    def test_decrypt_mcp_request(self):
        """Test MCP request decryption."""
        with tempfile.TemporaryDirectory() as temp_dir:
            sender = KeyManager(temp_dir, "sender")
            recipient = KeyManager(temp_dir, "recipient")
            
            original_data = {"request": "test request", "param": "value"}
            
            # Create encrypted request
            encrypted_request = create_encrypted_response(
                original_data,
                recipient.get_public_key_pem(),
                sender
            )
            
            # Decrypt request
            decrypted_data = decrypt_mcp_request(encrypted_request, recipient)
            
            assert decrypted_data == original_data
    
    def test_decrypt_non_encrypted_request(self):
        """Test error handling for non-encrypted requests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            recipient = KeyManager(temp_dir, "recipient")
            
            # Non-encrypted request
            request = {"encrypted": False, "data": "test"}
            
            with pytest.raises(ValueError, match="Request is not encrypted"):
                decrypt_mcp_request(request, recipient)


# Async test helper
@pytest.mark.asyncio
class TestAsyncFunctionality:
    """Test async components (would require actual MCP server instances)."""
    
    async def test_placeholder_async(self):
        """Placeholder for async tests that would require running servers."""
        # In a full test suite, this would test actual MCP server interactions
        # For now, just verify that async test infrastructure works
        await asyncio.sleep(0.001)
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
