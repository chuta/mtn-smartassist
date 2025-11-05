#!/bin/bash

# MTN SmartAssist - Quick Run Script
echo "🚀 Starting MTN SmartAssist..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating from template..."
    cp .env.example .env
    echo "Please edit .env and add your API key, then run this script again."
    exit 1
fi

# Activate virtual environment and run
echo "✅ Activating virtual environment..."
source venv/bin/activate

echo "✅ Starting Streamlit application..."
echo ""
echo "📱 MTN SmartAssist will open in your browser"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
