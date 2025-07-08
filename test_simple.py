#!/usr/bin/env python3
"""
Simple test to verify the MCP implementation is working.
This runs the corrected integration demo with proper error handling.
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    """Run a simple test of the integration demo."""
    print("🧪 Testing MCP SDK Implementation")
    print("="*50)
    
    try:
        # Import and run the fixed integration demo
        from integration_demo import run_integration_demo
        
        print("✅ Integration demo module imported successfully")
        print("🚀 Running integration demo...\n")
        
        await run_integration_demo()
        
        print("\n✅ Integration demo completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the mcp_sdk_implementation directory")
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 Troubleshooting:")
        print("1. Ensure virtual environment is activated")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Run individual client tests:")
        print("   python clients/simple_document_client.py")
        print("   python clients/simple_summarization_client.py")

if __name__ == "__main__":
    asyncio.run(main())
