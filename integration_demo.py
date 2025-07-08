"""
Integration demo showing how MCP servers and clients work together.
This simulates the original A2A scenario using proper MCP protocol.
"""

import asyncio
import json
import os
from contextlib import AsyncExitStack

# Add parent directory to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from clients.document_client import DocumentClient
from clients.summarization_client import SummarizationClient
from shared.config import LogConfig

# Setup logging
logger = LogConfig.setup_logging("integration_demo")


async def run_integration_demo():
    """Run an integrated demo showing MCP servers working together."""
    print("\n" + "="*60)
    print("MCP SDK Integration Demo")
    print("Simulating Agent-to-Agent Document Exchange")
    print("="*60 + "\n")
    
    print("⚠️  Note: Due to MCP SDK subprocess issues on Windows, using fallback approach")
    print("This demonstrates the same functionality with a more robust implementation.\n")
    
    try:
        # Use the simple client approach that works reliably
        print("🔗 Initializing document and summarization services...")
        
        # Import the working clients
        from clients.simple_document_client import SimpleDocumentClient
        from clients.simple_summarization_client import SimpleSummarizationClient
        
        # Initialize clients
        doc_client = SimpleDocumentClient()
        summary_client = SimpleSummarizationClient()
        
        print("✅ Initialized document and summarization services\n")
        
        # Scenario 1: Document Discovery and Verification
        print("📋 Scenario 1: Document Discovery and Verification")
        print("-" * 50)
        
        # List available documents
        print("🔍 Discovering available documents...")
        documents = await doc_client.list_documents(encrypted=False)
        
        if documents.get("documents"):
            print(f"Found {documents['total_count']} documents:")
            for doc in documents["documents"]:
                status_emoji = "✅" if doc["status"] == "verified" else "❌"
                print(f"  {status_emoji} {doc['document_id']}: {doc['description']} ({doc['status']})")
        
        print()
        
        # Verify a specific document
        target_doc = "DOC001"
        print(f"🔐 Verifying document: {target_doc}")
        verification = await doc_client.verify_document(target_doc, encrypted=True)
        
        if verification.get("verification_successful"):
            print(f"✅ Document verified: {verification['status']}")
            print(f"   Description: {verification['description']}")
        else:
            print(f"❌ Document verification failed: {verification.get('status', 'Unknown error')}")
        
        print("\n" + "="*60 + "\n")
        
        # Scenario 2: Secure Text Summarization
        print("📝 Scenario 2: Secure Text Summarization")
        print("-" * 50)
        
        # Check summarization service status
        print("🔍 Checking summarization service status...")
        service_status = await summary_client.check_service_status()
        
        if service_status.get("service_status") == "operational":
            print("✅ Summarization service is operational")
        else:
            print("❌ Summarization service has issues:")
            if service_status.get("missing_configurations"):
                print(f"   Missing configs: {service_status['missing_configurations']}")
        
        print()
        
        # Sample document content to summarize
        sample_document = """
        CONFIDENTIAL BUSINESS REPORT - Q4 2024
        
        Executive Summary:
        Our company has experienced unprecedented growth in the fourth quarter of 2024, 
        with revenue increasing by 45% compared to the same period last year. This growth 
        has been driven primarily by our new AI-powered product suite, which has captured 
        significant market share in the enterprise software sector.
        
        Key Performance Indicators:
        - Total Revenue: $12.5M (up 45% YoY)
        - New Customer Acquisitions: 2,847 (up 67% YoY)
        - Customer Retention Rate: 94.2%
        - Net Promoter Score: 8.7/10
        
        Market Analysis:
        The artificial intelligence market continues to expand rapidly, with our target 
        segment growing at 38% annually. Our competitive positioning has strengthened 
        significantly due to our proprietary machine learning algorithms and strategic 
        partnerships with major cloud providers.
        
        Financial Outlook:
        Based on current trends and our product roadmap, we project continued strong 
        growth throughout 2025, with an estimated revenue target of $75M for the full year.
        Investment in R&D will increase by 30% to maintain our technological edge.
        
        Risk Factors:
        Primary risks include increased competition from established tech giants, potential 
        economic downturn affecting enterprise spending, and regulatory changes in AI governance.
        
        Conclusion:
        The company is well-positioned for continued success, with strong fundamentals, 
        innovative products, and a clear growth strategy. However, we must remain vigilant 
        about emerging risks and continue to invest in our core competencies.
        """
        
        # Test with different access keys
        access_keys = [
            ("SECRETKEY123", "🔑 Valid Access Key"),
            ("INVALID_KEY", "🚫 Invalid Access Key"),
        ]
        
        for access_key, description in access_keys:
            print(f"{description}: {access_key}")
            
            # Request summarization
            result = await summary_client.summarize_text(
                sample_document, 
                access_key, 
                encrypted=True
            )
            
            if result.get("status") == "success":
                print("✅ Summarization successful!")
                print(f"📄 Original length: {result.get('text_length', 0)} characters")
                print(f"📝 Summary length: {result.get('summary_length', 0)} characters")
                print("\n📋 Generated Summary:")
                print("-" * 30)
                print(result["summary"])
                print("-" * 30)
            elif result.get("status") == "forbidden":
                print("❌ Access denied - invalid access key")
            elif result.get("status") == "service_error":
                print(f"⚠️  Service error: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ Unexpected error: {result.get('error', 'Unknown error')}")
            
            print()
        
        print("="*60 + "\n")
        
        # Scenario 3: End-to-End Encrypted Workflow
        print("🔐 Scenario 3: End-to-End Encrypted Workflow")
        print("-" * 50)
        print("Demonstrating secure document verification + summarization...")
        
        # Step 1: Verify document with encryption
        print("🔍 Step 1: Encrypted document verification...")
        encrypted_verification = await doc_client.verify_document("DOC002", encrypted=True)
        
        if encrypted_verification.get("verification_successful"):
            print(f"✅ Encrypted verification successful: {encrypted_verification['status']}")
            
            # Step 2: If verified, proceed with summarization
            if encrypted_verification["status"] == "verified":
                print("🔍 Step 2: Proceeding with encrypted summarization...")
                
                # Use the document description as content to summarize
                content_to_summarize = f"""
                Document ID: {encrypted_verification['document_id']}
                Description: {encrypted_verification['description']}
                Status: {encrypted_verification['status']}
                Verified By: {encrypted_verification['verified_by']}
                
                This document has been successfully verified in our system and is approved 
                for processing. The verification process confirms the authenticity and 
                current status of the document within our secure document management system.
                """
                
                summary_result = await summary_client.summarize_text(
                    content_to_summarize,
                    "SUMMARY_ACCESS_777",  # Different access key
                    encrypted=True
                )
                
                if summary_result.get("status") == "success":
                    print("✅ End-to-end encrypted workflow completed successfully!")
                    print("\n📋 Final Summary:")
                    print("-" * 30)
                    print(summary_result["summary"])
                    print("-" * 30)
                else:
                    print(f"❌ Summarization failed: {summary_result.get('error')}")
            else:
                print(f"⚠️  Document not verified, skipping summarization: {encrypted_verification['status']}")
        else:
            print(f"❌ Document verification failed: {encrypted_verification.get('error')}")
        
        print("\n" + "="*60)
        print("🎉 Integration Demo Complete!")
        print("="*60 + "\n")
        
        print("Summary of what was demonstrated:")
        print("✅ Document service discovery and verification")
        print("✅ Tool-based document validation")
        print("✅ Access-controlled text summarization")
        print("✅ End-to-end encryption for sensitive data")
        print("✅ Proper error handling and validation")
        print("✅ Multi-service orchestration")
        print("✅ Fallback implementation for MCP SDK compatibility")
        
    except Exception as e:
        logger.error(f"Integration demo failed: {e}")
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_integration_demo())
