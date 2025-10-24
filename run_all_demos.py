#!/usr/bin/env python3
"""
Run All Demos Script
This script runs all the demo applications in sequence for easy testing.
"""

import os
import sys
import time
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    load_dotenv()
    
    required_vars = [
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY", 
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file or environment.")
        return False
    
    return True

def run_demo(script_name, description):
    """Run a demo script and handle errors"""
    print(f"\n{'='*60}")
    print(f"🚀 Running: {description}")
    print(f"📄 Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        # Import and run the demo
        if script_name == "simple_chat_demo":
            import simple_chat_demo
            simple_chat_demo.run_conversation()
        elif script_name == "rag_demo":
            import rag_demo
            rag_demo.run_rag_demo()
        elif script_name == "langchain_demo":
            import langchain_demo
            langchain_demo.run_langchain_demo()
        else:
            print(f"❌ Unknown demo script: {script_name}")
            return False
        
        print(f"✅ {description} completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Main function to run all demos"""
    print("🎯 Langfuse Demo Suite")
    print("=====================")
    print("This script will run all demo applications in sequence.")
    print("Make sure you have a Langfuse cloud account at https://cloud.langfuse.com")
    print()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Define demos to run
    demos = [
        ("simple_chat_demo", "Simple Chat Demo"),
        ("rag_demo", "RAG (Retrieval Augmented Generation) Demo"),
        ("langchain_demo", "LangChain Integration Demo")
    ]
    
    # Run each demo
    successful_demos = 0
    total_demos = len(demos)
    
    for script_name, description in demos:
        if run_demo(script_name, description):
            successful_demos += 1
        
        # Add delay between demos
        if script_name != demos[-1][0]:  # Not the last demo
            print("\n⏳ Waiting 5 seconds before next demo...")
            time.sleep(5)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Demo Summary")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful_demos}/{total_demos}")
    print(f"❌ Failed: {total_demos - successful_demos}/{total_demos}")
    
    if successful_demos == total_demos:
        print("\n🎉 All demos completed successfully!")
        print("📊 Check your Langfuse dashboard at https://cloud.langfuse.com")
        print("   to see all the traces and analytics.")
    else:
        print(f"\n⚠️  {total_demos - successful_demos} demo(s) failed.")
        print("Check the error messages above for details.")
    
    print("\n📸 Screenshot Tips:")
    print("- Dashboard: Overview of all traces")
    print("- Trace Details: Individual request/response data")
    print("- Analytics: Token usage and performance metrics")
    print("- Sessions: Grouped conversations and workflows")

if __name__ == "__main__":
    main()
