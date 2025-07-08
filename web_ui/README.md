# MCP Document Exchange - Web UI

A modern web interface for the MCP-based Document Exchange and Summarization System.

## Features

- **Modern Design**: Inspired by the original agent_a_project but adapted for MCP integration
- **Dynamic Document Input**: Real-time text input with auto-resizing textarea
- **Multiple Processing Modes**:
  - **Verify & Summarize**: Full document processing pipeline
  - **Verify Only**: Document verification using access codes
  - **Summarize Only**: Text summarization without verification
- **Chat-style Activity Log**: Real-time display of system actions and responses
- **Service Health Monitoring**: Live status indicators for MCP services
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Features**: Sample document loading, result copying, etc.

## Architecture

```
web_ui/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── start_web_ui.bat      # Windows startup script
├── start_web_ui.sh       # Linux/macOS startup script
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── css/
    │   └── style.css     # Modern styling
    └── js/
        └── main.js       # Interactive functionality
```

## Quick Start

### Prerequisites

1. Python 3.8+ installed
2. MCP SDK implementation completed (servers and clients)
3. Access to the parent directory containing MCP clients

### Running the Web UI

**Windows:**
```bash
cd web_ui
start_web_ui.bat
```

**Linux/macOS:**
```bash
cd web_ui
chmod +x start_web_ui.sh
./start_web_ui.sh
```

**Manual Start:**
```bash
cd web_ui
python -m venv ../venv
source ../venv/bin/activate  # or ../venv/Scripts/activate on Windows
pip install -r requirements.txt
python app.py
```

### Access the Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Document Processing

1. **Select Processing Mode**:
   - **Verify & Summarize**: Complete processing pipeline
   - **Verify Only**: Document verification only
   - **Summarize Only**: Text summarization only

2. **Enter Content**:
   - Paste your document content in the text area
   - Enter the appropriate access code
   - Click the processing button

3. **Monitor Progress**:
   - Watch the activity log for real-time updates
   - Monitor service status indicators
   - View results in the modal popup

### Quick Actions

- **Load Sample Document**: Populate form with test data
- **System Health Check**: Verify MCP service status
- **Clear Logs**: Reset the activity display

### Access Codes

The system supports various access codes for different operations:
- `DOC001`: Standard document verification
- `VERIFY123`: Alternative verification code
- `SUMMARY456`: Summarization access code
- Custom codes as configured in your MCP servers

## API Endpoints

The web UI provides RESTful API endpoints:

### POST /api/verify_document
Verify a document using the MCP document verification service.

**Request:**
```json
{
  "document_content": "text content to verify",
  "access_code": "access code for verification"
}
```

### POST /api/summarize_text
Summarize text using the MCP summarization service.

**Request:**
```json
{
  "text_content": "text to summarize",
  "access_code": "access code for summarization"
}
```

### POST /api/process_document
Combined endpoint for document verification and summarization.

**Request:**
```json
{
  "document_content": "document content to process",
  "access_code": "access code for processing"
}
```

### GET /api/health
System health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "clients": {
    "document_client": true,
    "summarization_client": true
  },
  "timestamp": "2024-01-20T10:30:00"
}
```

## Configuration

### Environment Variables

- `FLASK_APP`: Application entry point (default: app.py)
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Enable debug mode (1/0)

### Customization

**Styling**: Modify `static/css/style.css` for custom themes
**Functionality**: Update `static/js/main.js` for behavior changes
**Templates**: Edit `templates/index.html` for layout modifications

## Architecture Integration

The web UI integrates with the MCP SDK implementation:

```
Web UI (Flask) → Simple Clients → MCP SDK → MCP Servers
```

### Client Integration

- **SimpleDocumentClient**: Direct function-based document verification
- **SimpleSummarizationClient**: Direct function-based text summarization
- **Fallback Support**: Robust error handling for Windows compatibility

### Security Features

- **Hybrid Encryption**: Secure communication between components
- **Access Control**: Code-based authorization for operations
- **Input Validation**: Server-side validation of all requests
- **Error Handling**: Comprehensive error reporting and logging

## Development

### Code Structure

**Backend (app.py)**:
- Flask application with RESTful API
- Integration with MCP simple clients
- Comprehensive error handling and logging
- Health monitoring and status reporting

**Frontend (JavaScript)**:
- Modern ES6+ JavaScript
- Async/await API communication
- Real-time UI updates
- Interactive form handling

**Styling (CSS)**:
- Modern CSS3 with gradients and animations
- Responsive design with Bootstrap integration
- Custom components and utilities
- Cross-browser compatibility

### Adding Features

1. **New Endpoints**: Add routes to `app.py`
2. **UI Components**: Extend `templates/index.html`
3. **Styling**: Add CSS to `static/css/style.css`
4. **Functionality**: Extend `static/js/main.js`

## Troubleshooting

### Common Issues

**Port 5000 in use:**
```bash
# Change port in app.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

**MCP clients not initialized:**
- Verify simple clients are available in `../clients/`
- Check that MCP SDK is properly installed
- Ensure server files exist in `../servers/`

**CSS not loading:**
- Clear browser cache
- Check Flask static file serving
- Verify file paths in templates

### Logs and Debugging

**Enable Flask debugging:**
```bash
export FLASK_DEBUG=1  # Linux/macOS
set FLASK_DEBUG=1     # Windows
```

**Check browser console:**
- Open Developer Tools (F12)
- Monitor JavaScript errors
- Check network requests

**Server logs:**
- Flask logs appear in terminal
- Check for client initialization errors
- Monitor API response codes

## Browser Compatibility

- **Chrome 80+**: Full support
- **Firefox 75+**: Full support
- **Safari 13+**: Full support (with webkit prefixes)
- **Edge 80+**: Full support

## Performance

- **Optimized Assets**: Minified CSS/JS in production
- **Efficient Updates**: DOM manipulation minimized
- **Responsive Loading**: Progressive enhancement
- **Caching**: Static asset caching enabled

## Security Considerations

- **Input Sanitization**: All user inputs validated
- **CORS Protection**: Cross-origin request controls
- **Session Management**: Secure session handling
- **Error Disclosure**: Limited error information exposure

For production deployment, consider:
- HTTPS/TLS encryption
- Reverse proxy configuration
- Rate limiting
- Security headers
