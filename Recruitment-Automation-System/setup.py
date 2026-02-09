#!/usr/bin/env python
"""
Setup script for the Recruitment Automation System.
Run this to initialize the project.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_project():
    """Initialize the project."""
    print("🚀 Setting up Recruitment Automation System...")
    
    # Create necessary directories
    directories = ['data', 'resumes', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("Creating .env from template...")
        
        if os.path.exists('.env.example'):
            os.system('copy .env.example .env' if os.name == 'nt' else 'cp .env.example .env')
            print("✅ .env file created from template")
            print("\n🔑 Please update your OpenAI API key in .env file")
        else:
            print("❌ .env.example not found!")
            sys.exit(1)
    else:
        print("✅ .env file exists")
    
    # Initialize database
    try:
        from src.database import Database
        db = Database()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)
    
    print("\n✅ Project setup complete!")
    print("\n📝 Next steps:")
    print("1. Update .env with your OpenAI API key")
    print("2. Run: streamlit run app.py")
    print("3. Upload resumes in the web interface")
    print("\nNeed help? Check README.md")

if __name__ == "__main__":
    setup_project()
