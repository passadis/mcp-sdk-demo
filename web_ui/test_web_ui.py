#!/usr/bin/env python3
"""
Test script for the MCP Document Exchange Web UI
This script tests the web interface functionality.
"""

import os
import sys
import time
import requests
import subprocess
import threading

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def test_web_ui():
    """Test the web UI functionality"""
    print("=== MCP Document Exchange Web UI Test ===")
    
    # Test 1: Check if Flask app starts
    print("\n1. Testing Flask application startup...")
    
    try:
        # Import and test the Flask app
        from app import app, initialize_clients
        
        print("✓ Flask app imported successfully")
        
        # Test client initialization
        print("\n2. Testing MCP client initialization...")
        if initialize_clients():
            print("✓ MCP clients initialized successfully")
        else:
            print("⚠ MCP clients initialization failed (expected if servers not running)")
        
        # Test 3: Check routes
        print("\n3. Testing Flask routes...")
        with app.test_client() as client:
            
            # Test main page
            response = client.get('/')
            print(f"GET / : {response.status_code}")
            
            # Test health endpoint
            response = client.get('/api/health')
            print(f"GET /api/health : {response.status_code}")
            print(f"Response: {response.get_json()}")
            
            # Test document verification (will fail without servers)
            test_data = {
                'document_content': 'Test document content',
                'access_code': 'DOC001'
            }
            
            response = client.post('/api/verify_document', 
                                 json=test_data,
                                 content_type='application/json')
            print(f"POST /api/verify_document : {response.status_code}")
            
            # Test summarization (will fail without servers)
            response = client.post('/api/summarize_text',
                                 json=test_data,
                                 content_type='application/json')
            print(f"POST /api/summarize_text : {response.status_code}")
            
            # Test full processing (will fail without servers)
            response = client.post('/api/process_document',
                                 json=test_data,
                                 content_type='application/json')
            print(f"POST /api/process_document : {response.status_code}")
        
        print("\n✓ All route tests completed")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_static_files():
    """Test static file availability"""
    print("\n4. Testing static files...")
    
    static_files = [
        'static/css/style.css',
        'static/js/main.js',
        'templates/index.html'
    ]
    
    for file_path in static_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")

def main():
    """Main test function"""
    print("Starting MCP Document Exchange Web UI tests...")
    
    # Test static files
    test_static_files()
    
    # Test web application
    if test_web_ui():
        print("\n🎉 Web UI tests completed successfully!")
        print("\nTo start the web UI manually:")
        print("1. cd web_ui")
        print("2. python app.py")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("\n❌ Web UI tests failed!")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
