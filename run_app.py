import subprocess
import sys
import os
from pathlib import Path

def main():
    print("Starting FinSolve Chatbot...")
    print("1. Installing dependencies...")
    
    # Install dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return

    # Check if .env file exists
    if not Path(".env").exists():
        print("\n⚠️  Warning: .env file not found!")
        print("Please create a .env file with your GROQ_API_KEY:")
        print("GROQ_API_KEY=your_api_key_here")
        print("\nYou can get a free API key from: https://console.groq.com/")
    
    print("\n2. Starting FastAPI server...")
    print("The server will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main() 