#!/usr/bin/env python3
"""
Setup script for MCP Document Exchange Web UI
Helps with environment configuration and installation.
"""

import os
import sys
import shutil

def banner():
    """Display setup banner"""
    print("=" * 60)
    print("🚀 MCP DOCUMENT EXCHANGE - WEB UI SETUP")
    print("=" * 60)
    print("This script will help you configure the environment")
    print("variables needed for the MCP Document Exchange System.")
    print("=" * 60)

def check_env_file():
    """Check if .env file exists"""
    env_file = '.env'
    example_file = '.env.example'
    
    if os.path.exists(env_file):
        print(f"✓ Found existing {env_file}")
        return True
    elif os.path.exists(example_file):
        print(f"📋 Found {example_file}")
        choice = input(f"Would you like to copy {example_file} to {env_file}? (y/n): ").lower()
        if choice in ['y', 'yes']:
            shutil.copy(example_file, env_file)
            print(f"✓ Created {env_file} from {example_file}")
            return True
    
    print(f"❌ No {env_file} file found")
    return False

def validate_azure_openai():
    """Validate Azure OpenAI configuration"""
    print("\n🔍 CHECKING AZURE OPENAI CONFIGURATION")
    print("-" * 40)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'AZURE_OPENAI_KEY': 'Your Azure OpenAI API key',
        'AZURE_OPENAI_ENDPOINT': 'Your Azure OpenAI endpoint URL',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'Your model deployment name'
    }
    
    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your-{var.lower().replace('_', '-')}-here":
            print(f"✓ {var}: {value[:20]}..." if len(value) > 20 else f"✓ {var}: {value}")
        else:
            print(f"❌ {var}: Not configured")
            missing.append((var, description))
    
    if missing:
        print(f"\n⚠ Missing {len(missing)} required environment variables:")
        for var, description in missing:
            print(f"   - {var}: {description}")
        print(f"\nPlease edit your .env file and add these variables.")
        return False
    else:
        print(f"\n✅ All Azure OpenAI variables configured!")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 INSTALLING DEPENDENCIES")
    print("-" * 40)
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_import():
    """Test if we can import required modules"""
    print("\n🧪 TESTING IMPORTS")
    print("-" * 40)
    
    modules = [
        ('flask', 'Flask web framework'),
        ('dotenv', 'Environment variable loader'),
        ('asyncio', 'Async support'),
    ]
    
    all_good = True
    for module, description in modules:
        try:
            __import__(module)
            print(f"✓ {module}: {description}")
        except ImportError:
            print(f"❌ {module}: {description} (not installed)")
            all_good = False
    
    return all_good

def show_next_steps():
    """Show next steps to user"""
    print("\n🎯 NEXT STEPS")
    print("-" * 40)
    print("1. Edit your .env file with your Azure OpenAI credentials:")
    print("   - Get API key from Azure Portal")
    print("   - Get endpoint URL from Azure Portal") 
    print("   - Set your model deployment name")
    print()
    print("2. Start the web UI:")
    print("   python app.py")
    print()
    print("3. Open your browser:")
    print("   http://localhost:5000")
    print()
    print("4. Test with sample data:")
    print("   - Click 'Load Sample Document'")
    print("   - Try access codes: DOC001, VERIFY123, SUMMARY456")

def main():
    """Main setup function"""
    banner()
    
    # Check .env file
    if not check_env_file():
        print("\n❌ Setup failed: No .env file available")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return 1
    
    # Test imports
    if not test_import():
        print("\n❌ Setup failed: Missing required modules")
        return 1
    
    # Validate configuration
    azure_configured = validate_azure_openai()
    
    if azure_configured:
        print("\n🎉 SETUP COMPLETE!")
        print("=" * 60)
        print("Your MCP Document Exchange Web UI is ready to run!")
        
        choice = input("\nWould you like to start the web UI now? (y/n): ").lower()
        if choice in ['y', 'yes']:
            print("\nStarting web UI...")
            os.system(f"{sys.executable} app.py")
    else:
        print("\n⚠ SETUP INCOMPLETE")
        print("=" * 60)
        print("Please configure your Azure OpenAI credentials in .env")
        
    show_next_steps()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user. Goodbye!")
        sys.exit(0)
