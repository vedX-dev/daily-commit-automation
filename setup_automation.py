#!/usr/bin/env python3
"""
Setup Script for Daily Commit Automation
========================================

This script helps set up the daily commit automation on different operating systems.
It provides interactive setup options and creates necessary configuration files.

Version: 1.0
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def detect_os():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def create_windows_batch_file(repo_path, python_path):
    """Create Windows batch file for startup"""
    batch_content = f"""@echo off
CHCP 65001 > NUL
cd /d "{repo_path}"
"{python_path}" daily_commit_automation.py
"""
    
    batch_file = Path(repo_path) / "daily_commit_launcher.bat"
    with open(batch_file, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Created Windows batch file: {batch_file}")
    print("To set up automatic startup:")
    print("1. Press Win+R, type 'shell:startup'")
    print("2. Copy the batch file to the startup folder")
    print("3. Or use Task Scheduler for more advanced options")

def check_git_setup(repo_path):
    """Check if git is properly set up"""
    try:
        # Check if it's a git repository
        result = subprocess.run(['git', 'status'], cwd=repo_path, 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not a git repository. Please initialize git first:")
            print(f"   cd {repo_path}")
            print("   git init")
            print("   git remote add origin <your-repo-url>")
            return False
        
        # Check for remote
        result = subprocess.run(['git', 'remote', '-v'], cwd=repo_path,
                              capture_output=True, text=True)
        if not result.stdout.strip():
            print("⚠️  No remote repository configured.")
            print("   Add a remote: git remote add origin <your-repo-url>")
        
        print("✅ Git repository looks good")
        return True
        
    except FileNotFoundError:
        print("❌ Git not found. Please install git first.")
        return False

def main():
    """Main setup function"""
    print("Daily Commit Automation Setup")
    print("=" * 40)
    
    # Get current directory
    repo_path = os.getcwd()
    print(f"Repository path: {repo_path}")
    
    # Check Python path
    python_path = sys.executable
    print(f"Python path: {python_path}")
    
    # Check git setup
    if not check_git_setup(repo_path):
        print("\nPlease set up git first, then run this script again.")
        return
    
    # Detect OS and create appropriate setup files
    os_type = detect_os()
    print(f"\nDetected OS: {os_type}")
    
    if os_type == "windows":
        create_windows_batch_file(repo_path, python_path)
        print("\nFor automation setup, please refer to the instructions above.")
    else:
        print("\nFor automation setup on non-Windows systems, please refer to the README.md for detailed instructions.")
    
    print("\n" + "=" * 40)
    print("Setup complete! Next steps:")
    print("1. Test the script: python daily_commit_automation.py")
    if os_type == "windows":
        print("2. Follow the Windows-specific instructions above to set up automatic startup.")
    else:
        print("2. Refer to README.md for automation setup instructions.")

if __name__ == "__main__":
    main()

