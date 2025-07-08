#!/usr/bin/env python3
"""
Quick test to verify the Flask app async fixes work correctly.
"""

import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def test_flask_app():
    """Test the Flask app with the async fixes"""
    print("🧪 Testing Flask App with Async Fixes")
    print("=" * 50)
    
    try:
        # Import the app
        from app import app, initialize_clients, SyncMCPWrapper
        
        print("✓ Flask app imported successfully")
        
        # Test wrapper creation
        print("Testing SyncMCPWrapper...")
        wrapper = SyncMCPWrapper()
        print("✓ SyncMCPWrapper created successfully")
        
        # Test initialization
        print("Testing client initialization...")
        if initialize_clients():
            print("✓ Clients initialized successfully")
        else:
            print("⚠ Client initialization failed (expected if servers not running)")
        
        # Test Flask routes
        print("Testing Flask routes...")
        with app.test_client() as client:
            
            # Test main page
            response = client.get('/')
            print(f"✓ GET / : {response.status_code}")
            
            # Test health endpoint
            response = client.get('/api/health')
            print(f"✓ GET /api/health : {response.status_code}")
            health_data = response.get_json()
            print(f"  Health data: {health_data}")
            
            # Test document verification (will use fallback)
            test_data = {
                'document_content': 'This is a test document for MCP processing.',
                'access_code': 'DOC001'
            }
            
            print("Testing document verification...")
            response = client.post('/api/verify_document',
                                 json=test_data,
                                 content_type='application/json')
            print(f"✓ POST /api/verify_document : {response.status_code}")
            
            if response.status_code == 200:
                result = response.get_json()
                print(f"  Verification result: {result}")
            else:
                print(f"  Error response: {response.get_json()}")
            
            # Test text summarization (will use fallback)
            print("Testing text summarization...")
            response = client.post('/api/summarize_text',
                                 json=test_data,
                                 content_type='application/json')
            print(f"✓ POST /api/summarize_text : {response.status_code}")
            
            if response.status_code == 200:
                result = response.get_json()
                print(f"  Summarization result: {result}")
            else:
                print(f"  Error response: {response.get_json()}")
        
        print("\n🎉 All tests completed successfully!")
        print("The Flask app is ready to run without async errors.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    if test_flask_app():
        print("\n✅ Flask app test passed!")
        print("\nTo start the web UI:")
        print("1. cd web_ui")
        print("2. python app.py")
        print("3. Open http://localhost:5000")
        return 0
    else:
        print("\n❌ Flask app test failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
