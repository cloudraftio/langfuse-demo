#!/bin/bash

# Langfuse Cloud Demo Setup Script
# This script helps you get started with the Langfuse cloud demo

set -e

echo "🚀 Setting up Langfuse Cloud Demo Environment"
echo "============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your actual API keys before running demos"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ pip is not installed. Please install pip and run: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Visit https://cloud.langfuse.com to create your Langfuse account"
echo "2. Get your API keys from Settings → API Keys"
echo "3. Update .env file with your keys"
echo "4. Run the demo scripts:"
echo "   - python simple_chat_demo.py"
echo "   - python rag_demo.py"
echo "   - python langchain_demo.py"
echo "   - python run_all_demos.py"
echo ""
echo "For more information, see README.md"
