"""
Complete Integration Demo for MCP Document Exchange Web UI

This script demonstrates the full integration between:
1. MCP-based document verification and summarization servers
2. Simple clients for direct function access
3. Modern web UI for user interaction

Run this to see the complete system in action.
"""

import os
import sys
import time
import json
import threading
import webbrowser
from datetime import datetime

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def banner():
    """Display welcome banner"""
    print("=" * 80)
    print("🚀 MCP DOCUMENT EXCHANGE - COMPLETE INTEGRATION DEMO")
    print("=" * 80)
    print("Modern Web UI + MCP SDK + Document Processing")
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def check_dependencies():
    """Check if all required components are available"""
    print("\n📋 DEPENDENCY CHECK")
    print("-" * 40)
    
    dependencies = {
        "Flask Web App": "app.py",
        "HTML Template": "templates/index.html", 
        "CSS Styling": "static/css/style.css",
        "JavaScript": "static/js/main.js",
        "Document Client": "../clients/simple_document_client.py",
        "Summarization Client": "../clients/simple_summarization_client.py",
        "Document Server": "../servers/document_verification_server/server.py",
        "Summarization Server": "../servers/summarization_server/server.py"
    }
    
    all_present = True
    for name, path in dependencies.items():
        full_path = os.path.join(current_dir, path)
        if os.path.exists(full_path):
            print(f"✓ {name}")
        else:
            print(f"✗ {name} (missing: {path})")
            all_present = False
    
    return all_present

def test_simple_clients():
    """Test the simple MCP clients directly"""
    print("\n🔧 TESTING MCP CLIENTS")
    print("-" * 40)
    
    try:
        # Test document client
        print("Testing Document Verification Client...")
        from clients.simple_document_client import SimpleDocumentClient
        
        doc_client = SimpleDocumentClient()
        doc_result = doc_client.verify_document("Test document content", "DOC001")
        print(f"✓ Document Client: {doc_result}")
        
    except Exception as e:
        print(f"⚠ Document Client: {e}")
    
    try:
        # Test summarization client
        print("Testing Summarization Client...")
        from clients.simple_summarization_client import SimpleSummarizationClient
        
        sum_client = SimpleSummarizationClient()
        sum_result = sum_client.summarize_text("This is a long text that needs summarization. It contains multiple sentences and should be processed by the MCP summarization service.", "SUMMARY001")
        print(f"✓ Summarization Client: {sum_result}")
        
    except Exception as e:
        print(f"⚠ Summarization Client: {e}")

def test_web_app():
    """Test the Flask web application"""
    print("\n🌐 TESTING WEB APPLICATION")
    print("-" * 40)
    
    try:
        from app import app, initialize_clients
        
        print("Importing Flask app...")
        print("✓ Flask app imported successfully")
        
        print("Initializing MCP wrapper...")
        if initialize_clients():
            print("✓ MCP wrapper initialized")
        else:
            print("⚠ MCP wrapper not fully available (servers may not be running)")
        
        print("Testing routes with test client...")
        with app.test_client() as client:
            # Test main page
            response = client.get('/')
            print(f"✓ GET / : Status {response.status_code}")
            
            # Test health check
            response = client.get('/api/health')
            health_data = response.get_json()
            print(f"✓ GET /api/health : {health_data}")
            
            # Test document verification with proper data
            test_data = {
                'document_content': 'Test document content for MCP processing',
                'access_code': 'DOC001'
            }
            
            response = client.post('/api/verify_document', 
                                 json=test_data,
                                 content_type='application/json')
            print(f"✓ POST /api/verify_document : Status {response.status_code}")
            if response.status_code == 200:
                result = response.get_json()
                print(f"  Response: {result.get('status', 'unknown')}")
            
        return True
        
    except Exception as e:
        print(f"✗ Web app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_ui_features():
    """Display information about UI features"""
    print("\n🎨 WEB UI FEATURES")
    print("-" * 40)
    
    features = [
        "📝 Dynamic document input with auto-resizing textarea",
        "🔑 Access code entry for secure processing",
        "⚙️ Multiple processing modes (Verify, Summarize, Both)",
        "💬 Chat-style activity log with real-time updates",
        "📊 Service health monitoring with status indicators", 
        "📱 Responsive design for desktop and mobile",
        "🎯 Quick actions (sample document, health check)",
        "📋 Copy results to clipboard functionality",
        "🎨 Modern gradient design with floating animations",
        "🔄 Auto-refresh health status every minute"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_api_endpoints():
    """Display available API endpoints"""
    print("\n🔗 API ENDPOINTS")
    print("-" * 40)
    
    endpoints = {
        "GET /": "Main web interface",
        "GET /api/health": "System health check",
        "POST /api/verify_document": "Document verification only",
        "POST /api/summarize_text": "Text summarization only", 
        "POST /api/process_document": "Full processing (verify + summarize)"
    }
    
    for endpoint, description in endpoints.items():
        print(f"  {endpoint:<30} - {description}")

def show_usage_instructions():
    """Show how to use the system"""
    print("\n📖 USAGE INSTRUCTIONS")
    print("-" * 40)
    
    instructions = [
        "1. Start the web UI: python app.py",
        "2. Open browser to: http://localhost:5000",
        "3. Select processing mode (Verify & Summarize, Verify Only, or Summarize Only)",
        "4. Enter document content in the text area",
        "5. Enter access code (try: DOC001, VERIFY123, SUMMARY456)",
        "6. Click the processing button",
        "7. Watch the activity log for real-time updates",
        "8. View results in the popup modal",
        "9. Use quick actions for testing and health checks"
    ]
    
    for instruction in instructions:
        print(f"  {instruction}")

def show_sample_data():
    """Show sample data for testing"""
    print("\n📄 SAMPLE TEST DATA")
    print("-" * 40)
    
    print("Sample Document Content:")
    print("=" * 20)
    sample_doc = """This is a comprehensive sample document for testing the MCP Document Exchange System.

The document contains multiple paragraphs with varied content to test both document verification and text summarization capabilities effectively.

Key components being tested:
- Document verification through MCP SDK with hybrid encryption
- Text summarization using AI services via MCP protocols
- Secure communication between web UI and backend services
- Access control mechanisms with code-based authorization
- Error handling and user feedback systems

This sample document is designed to be long enough to provide meaningful summarization results while remaining concise enough for quick testing during development and demonstration phases.

The system supports various access codes for different operational modes, allowing fine-grained control over document processing permissions and service access levels."""
    
    print(sample_doc)
    print("\nSample Access Codes:")
    print("- DOC001: Standard document verification")
    print("- VERIFY123: Alternative verification access") 
    print("- SUMMARY456: Summarization service access")

def start_web_ui_demo():
    """Instructions for starting the web UI"""
    print("\n🚀 STARTING WEB UI DEMO")
    print("-" * 40)
    
    print("To start the web interface:")
    print("1. Open a new terminal/command prompt")
    print("2. Navigate to the web_ui directory:")
    print("   cd mcp_sdk_implementation/web_ui")
    print("3. Run the application:")
    print("   python app.py")
    print("4. Open your browser to:")
    print("   http://localhost:5000")
    print()
    print("The web UI will be ready for interactive testing!")
    
    # Ask if user wants to auto-open browser
    try:
        choice = input("\nWould you like to open the browser automatically? (y/n): ").lower()
        if choice in ['y', 'yes']:
            print("Opening browser in 3 seconds...")
            time.sleep(3)
            webbrowser.open('http://localhost:5000')
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")

def main():
    """Main demo function"""
    banner()
    
    # Check if all components are available
    if not check_dependencies():
        print("\n❌ Some components are missing. Please ensure all files are present.")
        return 1
    
    print("\n✅ All components found!")
    
    # Test MCP clients
    test_simple_clients()
    
    # Test web application
    if not test_web_app():
        print("\n❌ Web application test failed!")
        return 1
    
    print("\n✅ Web application test passed!")
    
    # Show features and usage
    show_ui_features()
    show_api_endpoints()
    show_usage_instructions()
    show_sample_data()
    
    # Instructions for starting demo
    start_web_ui_demo()
    
    print("\n" + "=" * 80)
    print("🎉 MCP DOCUMENT EXCHANGE DEMO COMPLETE!")
    print("=" * 80)
    print("System is ready for interactive testing via the web interface.")
    print("Thank you for trying the MCP Document Exchange System!")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Goodbye!")
        sys.exit(0)
