#!/usr/bin/env python3
"""
Script to install required dependencies for the Wizzers backend.
Run this script to install all necessary packages.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements from requirements.txt"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print("Error: requirements.txt not found!")
        return False
    
    try:
        print("Installing Python dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Installing Wizzers Backend Dependencies...")
    success = install_requirements()
    
    if success:
        print("\n🎉 Setup complete! You can now run the Flask app with:")
        print("   python app.py")
    else:
        print("\n💥 Setup failed. Please check the error messages above.")
        sys.exit(1)
