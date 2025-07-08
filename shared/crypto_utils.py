"""
Shared cryptographic utilities for secure communication between MCP servers and clients.
Maintains compatibility with the original hybrid encryption implementation.
"""

import os
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Tuple, Dict, Any


class HybridCrypto:
    """Hybrid encryption using RSA + AES-GCM for secure message exchange."""
    
    @staticmethod
    def generate_key_pair() -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """Generate a new RSA key pair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def save_key_pair(private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey, 
                      key_dir: str, key_name: str) -> Tuple[str, str]:
        """Save key pair to PEM files."""
        os.makedirs(key_dir, exist_ok=True)
        
        private_path = os.path.join(key_dir, f'{key_name}_private.pem')
        public_path = os.path.join(key_dir, f'{key_name}_public.pem')
        
        # Save private key
        with open(private_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Save public key
        with open(public_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        return private_path, public_path
    
    @staticmethod
    def load_private_key(path: str) -> rsa.RSAPrivateKey:
        """Load private key from PEM file."""
        with open(path, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None)
    
    @staticmethod
    def load_public_key(path: str) -> rsa.RSAPublicKey:
        """Load public key from PEM file."""
        with open(path, "rb") as key_file:
            return serialization.load_pem_public_key(key_file.read())
    
    @staticmethod
    def public_key_to_pem_string(public_key: rsa.RSAPublicKey) -> str:
        """Convert public key to PEM string."""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    
    @staticmethod
    def public_key_from_pem_string(pem_string: str) -> rsa.RSAPublicKey:
        """Load public key from PEM string."""
        return serialization.load_pem_public_key(pem_string.encode())
    
    @staticmethod
    def encrypt_message(message: str, recipient_public_key: rsa.RSAPublicKey) -> str:
        """
        Encrypt message using hybrid encryption (RSA + AES-GCM).
        Returns JSON string with encrypted components.
        """
        try:
            # Generate AES key
            aes_key = AESGCM.generate_key(bit_length=256)
            
            # Encrypt AES key with RSA
            encrypted_aes_key = recipient_public_key.encrypt(
                aes_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Encrypt message with AES-GCM
            aesgcm = AESGCM(aes_key)
            nonce = os.urandom(12)  # GCM standard nonce size
            ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
            
            # Package for transmission
            payload = {
                "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode('utf-8'),
                "nonce": base64.b64encode(nonce).decode('utf-8'),
                "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
            }
            
            return json.dumps(payload)
            
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}")
    
    @staticmethod
    def decrypt_message(encrypted_payload: str, private_key: rsa.RSAPrivateKey) -> str:
        """
        Decrypt message using hybrid decryption.
        Takes JSON string with encrypted components.
        """
        try:
            # Parse encrypted payload
            payload = json.loads(encrypted_payload)
            encrypted_aes_key = base64.b64decode(payload['encrypted_aes_key'])
            nonce = base64.b64decode(payload['nonce'])
            ciphertext = base64.b64decode(payload['ciphertext'])
            
            # Decrypt AES key with RSA
            aes_key = private_key.decrypt(
                encrypted_aes_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decrypt message with AES-GCM
            aesgcm = AESGCM(aes_key)
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            
            return decrypted_bytes.decode()
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")


class KeyManager:
    """Manages cryptographic keys for MCP servers and clients."""
    
    def __init__(self, key_dir: str, entity_name: str):
        self.key_dir = key_dir
        self.entity_name = entity_name
        self.private_key_path = os.path.join(key_dir, f'{entity_name}_private.pem')
        self.public_key_path = os.path.join(key_dir, f'{entity_name}_public.pem')
        
        self.private_key = None
        self.public_key = None
        
        self._load_or_generate_keys()
    
    def _load_or_generate_keys(self):
        """Load existing keys or generate new ones."""
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            # Load existing keys
            self.private_key = HybridCrypto.load_private_key(self.private_key_path)
            self.public_key = HybridCrypto.load_public_key(self.public_key_path)
            print(f"Loaded existing keys for {self.entity_name}")
        else:
            # Generate new keys
            self.private_key, self.public_key = HybridCrypto.generate_key_pair()
            HybridCrypto.save_key_pair(
                self.private_key, 
                self.public_key, 
                self.key_dir, 
                self.entity_name
            )
            print(f"Generated new keys for {self.entity_name}")
    
    def get_public_key_pem(self) -> str:
        """Get public key as PEM string."""
        return HybridCrypto.public_key_to_pem_string(self.public_key)
    
    def encrypt_for_recipient(self, message: str, recipient_public_key_pem: str) -> str:
        """Encrypt message for a specific recipient."""
        recipient_public_key = HybridCrypto.public_key_from_pem_string(recipient_public_key_pem)
        return HybridCrypto.encrypt_message(message, recipient_public_key)
    
    def decrypt_message(self, encrypted_payload: str) -> str:
        """Decrypt message intended for this entity."""
        return HybridCrypto.decrypt_message(encrypted_payload, self.private_key)


# Access control utilities
class AccessControl:
    """Handles access control for MCP servers."""
    
    @staticmethod
    def validate_access_key(access_key: str, valid_keys: list) -> bool:
        """Validate if access key is authorized."""
        return access_key in valid_keys
    
    @staticmethod
    def generate_access_key() -> str:
        """Generate a new access key."""
        return base64.b64encode(os.urandom(32)).decode('utf-8')[:32]


# Utility functions for MCP tool responses
def create_encrypted_response(data: Dict[Any, Any], recipient_public_key_pem: str, 
                            sender_key_manager: KeyManager) -> Dict[str, Any]:
    """Create an encrypted response for MCP tools."""
    response_json = json.dumps(data)
    encrypted_payload = sender_key_manager.encrypt_for_recipient(
        response_json, 
        recipient_public_key_pem
    )
    
    return {
        "encrypted": True,
        "payload": encrypted_payload,
        "sender_public_key": sender_key_manager.get_public_key_pem()
    }


def decrypt_mcp_request(encrypted_request: Dict[str, Any], 
                       key_manager: KeyManager) -> Dict[Any, Any]:
    """Decrypt an encrypted MCP request."""
    if not encrypted_request.get("encrypted", False):
        raise ValueError("Request is not encrypted")
    
    encrypted_payload = encrypted_request.get("payload")
    if not encrypted_payload:
        raise ValueError("No encrypted payload found")
    
    decrypted_json = key_manager.decrypt_message(encrypted_payload)
    return json.loads(decrypted_json)
