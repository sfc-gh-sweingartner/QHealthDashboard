#!/usr/bin/env python3
"""
Quantium Healthcare Analytics Platform - Launch Script
Automated setup and launch for the Streamlit dashboard application
"""

import subprocess
import sys
import os
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_requirements():
    """Check if requirements are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import snowflake.connector
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("📦 Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def check_secrets_file():
    """Check if Snowflake secrets are configured"""
    secrets_path = ".streamlit/secrets.toml"
    if os.path.exists(secrets_path):
        print("✅ Snowflake secrets file found")
        return True
    else:
        print("⚠️  Snowflake secrets not configured")
        print("📝 Please copy .streamlit/secrets.toml.template to .streamlit/secrets.toml")
        print("   and fill in your Snowflake credentials")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching Quantium Healthcare Analytics Platform...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("⏱️  Loading time target: <5 seconds")
    print("🤖 AI features powered by Snowflake Cortex")
    print("\n" + "="*60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

def main():
    """Main setup and launch sequence"""
    print("🏥 Quantium Healthcare Analytics Platform")
    print("🎯 Mission: <5 second dashboards with AI capabilities")
    print("="*60)
    
    # Run checks
    if not check_python_version():
        return
        
    if not check_requirements():
        print("❌ Failed to install requirements")
        return
        
    secrets_ok = check_secrets_file()
    
    print("\n📋 Pre-flight Check Complete")
    print("="*30)
    
    if not secrets_ok:
        response = input("Continue without Snowflake connection? (y/N): ")
        if response.lower() != 'y':
            print("👋 Setup your Snowflake credentials and try again")
            return
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()