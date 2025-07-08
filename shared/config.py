"""
Shared configuration for MCP servers and clients.
Centralizes environment variables and common settings.
"""

import os
from typing import Optional, List


class Config:
    """Configuration management for MCP implementation."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT") 
    AZURE_OPENAI_DEPLOYMENT_NAME: Optional[str] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    # MCP Server Configuration
    DOCUMENT_SERVER_HOST: str = os.getenv("DOCUMENT_SERVER_HOST", "localhost")
    DOCUMENT_SERVER_PORT: int = int(os.getenv("DOCUMENT_SERVER_PORT", "8001"))
    
    SUMMARIZATION_SERVER_HOST: str = os.getenv("SUMMARIZATION_SERVER_HOST", "localhost")
    SUMMARIZATION_SERVER_PORT: int = int(os.getenv("SUMMARIZATION_SERVER_PORT", "8002"))
    
    # Key Management
    KEYS_BASE_DIR: str = os.getenv("KEYS_BASE_DIR", "keys")
    
    # Access Control
    VALID_ACCESS_KEYS: List[str] = os.getenv(
        "VALID_ACCESS_KEYS", 
        "DOC001,SECRETKEY123,SUMMARY_ACCESS_777"
    ).split(",")
    
    # Document Store (for verification server)
    VALID_DOCUMENTS: dict = {
        "DOC001": {
            "status": "verified",
            "description": "Contract Agreement 2024",
            "verified_by": "Agent B"
        },
        "DOC002": {
            "status": "verified", 
            "description": "Financial Report Q4",
            "verified_by": "Agent B"
        },
        "DOC003": {
            "status": "revoked",
            "description": "Outdated Policy Document",
            "verified_by": "Agent B"
        },
    }
    
    @classmethod
    def validate_azure_openai_config(cls) -> tuple[bool, List[str]]:
        """Validate Azure OpenAI configuration."""
        missing = []
        
        if not cls.AZURE_OPENAI_API_KEY:
            missing.append("AZURE_OPENAI_KEY")
        if not cls.AZURE_OPENAI_ENDPOINT:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not cls.AZURE_OPENAI_DEPLOYMENT_NAME:
            missing.append("AZURE_OPENAI_DEPLOYMENT_NAME")
            
        return len(missing) == 0, missing
    
    @classmethod
    def get_server_info(cls, server_type: str) -> dict:
        """Get server connection information."""
        if server_type == "document":
            return {
                "host": cls.DOCUMENT_SERVER_HOST,
                "port": cls.DOCUMENT_SERVER_PORT,
                "url": f"http://{cls.DOCUMENT_SERVER_HOST}:{cls.DOCUMENT_SERVER_PORT}"
            }
        elif server_type == "summarization":
            return {
                "host": cls.SUMMARIZATION_SERVER_HOST,
                "port": cls.SUMMARIZATION_SERVER_PORT,
                "url": f"http://{cls.SUMMARIZATION_SERVER_HOST}:{cls.SUMMARIZATION_SERVER_PORT}"
            }
        else:
            raise ValueError(f"Unknown server type: {server_type}")


class LogConfig:
    """Logging configuration."""
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def setup_logging(cls, logger_name: str):
        """Setup logging for MCP components."""
        import logging
        
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format=cls.LOG_FORMAT
        )
        
        return logging.getLogger(logger_name)
