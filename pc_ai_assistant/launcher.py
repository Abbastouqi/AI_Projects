#!/usr/bin/env python
"""
PC AI Assistant Launcher
Runs the web frontend on port 5000 and opens browser automatically
"""
import os
import sys
import webbrowser
import time
from web_frontend import app

if __name__ == '__main__':
    print("=" * 60)
    print("PC AI ASSISTANT - ADMISSIONS AUTOMATION")
    print("=" * 60)
    print("\n✅ Starting server...")
    print("📱 Open your browser to: http://127.0.0.1:5000")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    # Open browser after a short delay
    time.sleep(2)
    try:
        webbrowser.open("http://127.0.0.1:5000", new=2)
        print("🌐 Browser opened automatically\n")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}\n")
    
    # Run the Flask app
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)
