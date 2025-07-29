#!/usr/bin/env python3
"""
Script to set up git repository for deployment.
"""
import subprocess
import os
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_git():
    """Set up git repository for deployment."""
    print("🚀 Setting up Git repository for deployment...")
    print()
    
    # Check if git is installed
    if not run_command("git --version", "Checking git installation"):
        print("❌ Git is not installed. Please install git first.")
        return False
    
    # Initialize git repository
    if not os.path.exists(".git"):
        if not run_command("git init", "Initializing git repository"):
            return False
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Create initial commit
    if not run_command('git commit -m "Initial commit: Smallcase Portfolio Rebalancer"', "Creating initial commit"):
        return False
    
    print()
    print("✅ Git repository setup completed!")
    print()
    print("📋 Next steps:")
    print("1. Create a new repository on GitHub")
    print("2. Add your GitHub repository as remote:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git")
    print("3. Push to GitHub:")
    print("   git push -u origin main")
    print("4. Deploy to Streamlit Cloud:")
    print("   - Go to https://share.streamlit.io")
    print("   - Sign in with GitHub")
    print("   - Click 'New app'")
    print("   - Select your repository")
    print("   - Set main file path to: main.py")
    print("   - Click 'Deploy'")
    print()
    print("🌐 Your app will be live at: https://your-app-name.streamlit.app")
    
    return True

if __name__ == "__main__":
    setup_git() 