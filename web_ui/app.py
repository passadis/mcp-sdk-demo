"""
Modern Web UI for MCP-based Document Exchange and Summarization System

This Flask application provides a web interface for:
1. Dynamic document input and access code entry
2. Document verification through MCP SDK
3. Text summarization through MCP SDK  
4. Chat-style interaction display

Based on the original agent_a_project design but adapted for MCP integration.
"""

import os
import sys
import json
import traceback
import asyncio
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import logging

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Environment variables loaded from .env file")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠ Proceeding with system environment variables only")

# Add the parent directory to Python path to import our clients
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import our MCP clients
from clients.simple_document_client import SimpleDocumentClient
from clients.simple_summarization_client import SimpleSummarizationClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'mcp-ui-secret-key-change-in-production')

# Synchronous wrapper for MCP clients
class SyncMCPWrapper:
    """Synchronous wrapper for async MCP clients"""
    
    def __init__(self):
        self.document_client = SimpleDocumentClient()
        self.summarization_client = SimpleSummarizationClient()
    
    def verify_document(self, document_content: str, access_code: str) -> dict:
        """Synchronous document verification"""
        try:
            # Create a hash of the document content to use as document_id
            import hashlib
            document_id = hashlib.md5(document_content.encode()).hexdigest()[:8]
            
            # Run async verification
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.document_client.verify_document(access_code, encrypted=False)
                )
                # Add document content info to result
                result['document_content_hash'] = document_id
                result['access_code'] = access_code
                result['verified'] = result.get('verification_successful', False)
                return result
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Document verification error: {e}")
            return {
                'verified': False,
                'error': str(e),
                'message': f'Document verification failed: {str(e)}'
            }
    
    def summarize_text(self, text_content: str, access_code: str) -> dict:
        """Synchronous text summarization"""
        try:
            # Run async summarization
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.summarization_client.summarize_text(text_content, access_code, encrypted=False)
                )
                return result
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Text summarization error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Text summarization failed: {str(e)}'
            }

# Initialize MCP wrapper
mcp_wrapper = None

def initialize_clients():
    """Initialize MCP clients with error handling"""
    global mcp_wrapper
    
    try:
        logger.info("Initializing MCP wrapper...")
        
        # Check Azure OpenAI configuration
        azure_config = check_azure_openai_config()
        if not azure_config['valid']:
            logger.warning("Azure OpenAI configuration incomplete:")
            for missing in azure_config['missing']:
                logger.warning(f"  - Missing: {missing}")
            logger.warning("Some functionality may be limited without proper Azure OpenAI configuration")
        
        # Initialize synchronous MCP wrapper
        mcp_wrapper = SyncMCPWrapper()
        logger.info("MCP wrapper initialized successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize MCP wrapper: {e}")
        logger.error(traceback.format_exc())
        return False

def check_azure_openai_config():
    """Check if Azure OpenAI configuration is complete"""
    required_vars = {
        'AZURE_OPENAI_KEY': os.getenv('AZURE_OPENAI_KEY'),
        'AZURE_OPENAI_ENDPOINT': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'AZURE_OPENAI_DEPLOYMENT_NAME': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    }
    
    missing = [var for var, value in required_vars.items() if not value]
    
    return {
        'valid': len(missing) == 0,
        'missing': missing,
        'config': required_vars
    }

@app.route('/')
def index():
    """Main page with document input interface"""
    return render_template('index.html')

@app.route('/api/verify_document', methods=['POST'])
def verify_document():
    """
    Verify a document using the MCP document verification service
    
    Expected JSON payload:
    {
        "document_content": "text content to verify",
        "access_code": "access code for verification"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'No JSON data provided'
            }), 400
            
        document_content = data.get('document_content', '').strip()
        access_code = data.get('access_code', '').strip()
        
        if not document_content or not access_code:
            return jsonify({
                'status': 'error', 
                'error': 'Both document content and access code are required'
            }), 400
            
        logger.info(f"Verifying document with access code: {access_code}")
        
        # Use the MCP wrapper for verification
        if not mcp_wrapper:
            logger.error("MCP wrapper not initialized")
            return jsonify({
                'status': 'error',
                'error': 'Document verification service not available'
            }), 503
            
        # Perform document verification
        result = mcp_wrapper.verify_document(document_content, access_code)
        
        logger.info(f"Document verification result: {result}")
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in document verification: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'error': f'Document verification failed: {str(e)}'
        }), 500

@app.route('/api/summarize_text', methods=['POST'])
def summarize_text():
    """
    Summarize text using the MCP summarization service
    
    Expected JSON payload:
    {
        "text_content": "text to summarize", 
        "access_code": "access code for summarization"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'No JSON data provided'
            }), 400
            
        text_content = data.get('text_content', '').strip()
        access_code = data.get('access_code', '').strip()
        
        if not text_content or not access_code:
            return jsonify({
                'status': 'error',
                'error': 'Both text content and access code are required'
            }), 400
            
        logger.info(f"Summarizing text with access code: {access_code}")
        
        # Use the MCP wrapper
        if not mcp_wrapper:
            logger.error("MCP wrapper not initialized")
            return jsonify({
                'status': 'error',
                'error': 'Summarization service not available'
            }), 503
            
        # Perform text summarization
        result = mcp_wrapper.summarize_text(text_content, access_code)
        
        logger.info(f"Text summarization result received")
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in text summarization: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'error': f'Text summarization failed: {str(e)}'
        }), 500

@app.route('/api/process_document', methods=['POST'])
def process_document():
    """
    Combined endpoint that first verifies a document, then summarizes it if verified
    
    Expected JSON payload:
    {
        "document_content": "document content to process",
        "access_code": "access code for processing"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'No JSON data provided'
            }), 400
            
        document_content = data.get('document_content', '').strip()
        access_code = data.get('access_code', '').strip()
        
        if not document_content or not access_code:
            return jsonify({
                'status': 'error',
                'error': 'Both document content and access code are required'
            }), 400
            
        logger.info(f"Processing document with access code: {access_code}")
        
        # Check if wrapper is available
        if not mcp_wrapper:
            logger.error("MCP wrapper not initialized")
            return jsonify({
                'status': 'error',
                'error': 'Document processing services not available'
            }), 503
        
        # Step 1: Verify document
        logger.info("Step 1: Verifying document...")
        verification_result = mcp_wrapper.verify_document(document_content, access_code)
        
        # Step 2: If verified, summarize
        if verification_result.get('verified', False):
            logger.info("Step 2: Document verified, proceeding with summarization...")
            summarization_result = mcp_wrapper.summarize_text(document_content, access_code)
            
            return jsonify({
                'status': 'success',
                'verification': verification_result,
                'summarization': summarization_result,
                'timestamp': datetime.now().isoformat()
            })
        else:
            logger.info("Document verification failed")
            return jsonify({
                'status': 'verification_failed',
                'verification': verification_result,
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Error in document processing: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'error': f'Document processing failed: {str(e)}'
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if clients are initialized and working
        client_status = {
            'document_client': mcp_wrapper is not None,
            'summarization_client': mcp_wrapper is not None
        }
        
        # Check Azure OpenAI configuration
        azure_config = check_azure_openai_config()
        
        return jsonify({
            'status': 'healthy' if azure_config['valid'] else 'warning',
            'clients': client_status,
            'azure_openai': {
                'configured': azure_config['valid'],
                'missing_vars': azure_config['missing'] if not azure_config['valid'] else []
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Initialize MCP wrapper
    if initialize_clients():
        logger.info("Starting MCP Web UI...")
        
        # Get configuration from environment
        host = os.getenv('WEB_UI_HOST', '0.0.0.0')
        port = int(os.getenv('WEB_UI_PORT', '5000'))
        debug = os.getenv('FLASK_DEBUG', '1') == '1'
        
        logger.info(f"Web UI will be available at: http://localhost:{port}")
        app.run(host=host, port=port, debug=debug)
    else:
        logger.error("Failed to initialize MCP wrapper. Exiting.")
        logger.error("Please check your .env file configuration.")
        sys.exit(1)
