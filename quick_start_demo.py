"""
Quick Start Demo - MCP SDK Implementation with Fallback

This script demonstrates the MCP SDK implementation with error handling
and fallback to simplified approaches if MCP SDK has issues.
"""

import asyncio
import json
import os
import sys
import traceback

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.config import Config, LogConfig
from shared.crypto_utils import KeyManager

# Setup logging
logger = LogConfig.setup_logging("quick_start_demo")

async def test_mcp_sdk_approach():
    """Test the full MCP SDK approach."""
    print("🔍 Testing MCP SDK Approach...")
    
    try:
        from clients.document_client import DocumentClient
        from clients.summarization_client import SummarizationClient
        
        # Test document client
        doc_client = DocumentClient()
        
        # Simple test - just try to initialize
        print("✅ MCP SDK clients imported successfully")
        
        # For now, we'll skip the actual connection test due to the known issue
        print("⚠️  MCP SDK connection test skipped due to known issues")
        return False
        
    except Exception as e:
        print(f"❌ MCP SDK approach failed: {e}")
        return False

async def test_simple_approach():
    """Test the simplified approach."""
    print("🔍 Testing Simplified Approach...")
    
    try:
        from clients.simple_document_client import SimpleDocumentClient
        
        client = SimpleDocumentClient()
        
        # Test document listing
        documents = await client.list_documents()
        print(f"✅ Found {documents.get('total_count', 0)} documents")
        
        # Test document verification
        result = await client.verify_document("DOC001")
        if result.get("verification_successful"):
            print(f"✅ Document verification successful: {result['status']}")
        else:
            print(f"❌ Document verification failed: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simplified approach failed: {e}")
        traceback.print_exc()
        return False

async def test_direct_approach():
    """Test direct configuration access."""
    print("🔍 Testing Direct Configuration Access...")
    
    try:
        # Test configuration access
        documents = Config.VALID_DOCUMENTS
        print(f"✅ Configuration loaded: {len(documents)} documents available")
        
        # Test key management
        key_manager = KeyManager(
            key_dir=os.path.join(Config.KEYS_BASE_DIR, "test_client"),
            entity_name="test_client"
        )
        
        public_key = key_manager.get_public_key_pem()
        print(f"✅ Key management working: {len(public_key)} character public key")
        
        # Test Azure OpenAI configuration
        config_valid, missing = Config.validate_azure_openai_config()
        if config_valid:
            print("✅ Azure OpenAI configuration is complete")
        else:
            print(f"⚠️  Azure OpenAI configuration missing: {missing}")
            print("   (This is expected if you haven't configured Azure OpenAI)")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct approach failed: {e}")
        traceback.print_exc()
        return False

async def demo_document_workflow():
    """Demonstrate the document workflow using available methods."""
    print("\n" + "="*60)
    print("📋 Document Workflow Demo")
    print("="*60)
    
    try:
        # Use the simple client for demonstration
        from clients.simple_document_client import SimpleDocumentClient
        
        client = SimpleDocumentClient()
        
        # Step 1: List all documents
        print("\n1. 📋 Listing Available Documents:")
        documents = await client.list_documents()
        
        if documents.get("documents"):
            for doc in documents["documents"]:
                status_emoji = "✅" if doc["status"] == "verified" else "❌"
                print(f"   {status_emoji} {doc['document_id']}: {doc['description']}")
        
        # Step 2: Verify each document
        print("\n2. 🔍 Verifying Documents:")
        for doc_id in ["DOC001", "DOC002", "DOC003", "INVALID_DOC"]:
            result = await client.verify_document(doc_id)
            
            if result.get("verification_successful"):
                print(f"   ✅ {doc_id}: {result['status']} - {result['description']}")
            else:
                print(f"   ❌ {doc_id}: {result.get('status', 'error')}")
        
        # Step 3: Demonstrate key management
        print("\n3. 🔐 Security Features:")
        key_manager = KeyManager(
            key_dir=os.path.join(Config.KEYS_BASE_DIR, "demo_client"),
            entity_name="demo_client"
        )
        
        public_key = key_manager.get_public_key_pem()
        print(f"   ✅ Client public key generated ({len(public_key)} chars)")
        
        # Test encryption/decryption
        test_message = "This is a test message for encryption"
        try:
            encrypted = key_manager.encrypt_for_recipient(test_message, public_key)
            decrypted = key_manager.decrypt_message(encrypted)
            
            if decrypted == test_message:
                print("   ✅ Encryption/decryption working correctly")
            else:
                print("   ❌ Encryption/decryption failed")
        except Exception as e:
            print(f"   ❌ Encryption test failed: {e}")
        
        print("\n✅ Document workflow demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Document workflow demo failed: {e}")
        traceback.print_exc()

async def main():
    """Run the quick start demo."""
    print("🚀 MCP SDK Implementation - Quick Start Demo")
    print("="*60)
    
    print("This demo will test different approaches to verify the implementation works.")
    print("Some approaches may fail due to MCP SDK compatibility issues.")
    print("That's expected - we'll show you what works!\n")
    
    # Test different approaches
    approaches = [
        ("MCP SDK", test_mcp_sdk_approach),
        ("Simplified", test_simple_approach),
        ("Direct Config", test_direct_approach),
    ]
    
    working_approaches = []
    
    for name, test_func in approaches:
        print(f"\n{'='*30}")
        print(f"Testing {name} Approach")
        print(f"{'='*30}")
        
        success = await test_func()
        if success:
            working_approaches.append(name)
            print(f"✅ {name} approach is working!")
        else:
            print(f"❌ {name} approach has issues")
    
    print(f"\n{'='*60}")
    print("📊 Summary")
    print(f"{'='*60}")
    
    if working_approaches:
        print(f"✅ Working approaches: {', '.join(working_approaches)}")
        print("\nProceeding with document workflow demo using available methods...")
        await demo_document_workflow()
    else:
        print("❌ No approaches are working. Please check the troubleshooting guide.")
    
    print(f"\n{'='*60}")
    print("🎉 Quick Start Demo Complete!")
    print(f"{'='*60}")
    
    print("\nNext steps:")
    print("1. Check TROUBLESHOOTING.md for resolving any issues")
    print("2. Use the working approaches for your implementation")
    print("3. Configure Azure OpenAI for summarization features")
    print("4. Review the code in the clients/ and servers/ directories")

if __name__ == "__main__":
    asyncio.run(main())
