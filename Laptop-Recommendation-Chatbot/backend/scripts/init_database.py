"""
Script to initialize the database with tables and sample data
Run this after setting up your environment
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.seed_data import seed_database

if __name__ == "__main__":
    print("Initializing database...")
    seed_database()
    print("\nDatabase initialization complete!")
    print("\nYou can now start the FastAPI server with: python main.py")
