#!/bin/bash

# MTN SmartAssist - Streamlit Cloud Deployment Script

echo "🚀 Preparing MTN SmartAssist for Streamlit Cloud Deployment..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git branch -M main
fi

# Check if .streamlit/secrets.toml exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  Warning: .streamlit/secrets.toml not found!"
    echo "Please create it with your API keys before deploying."
    echo ""
    echo "Example content:"
    echo '[secrets]'
    echo 'OPENAI_API_KEY = "sk-proj-your-key-here"'
    echo ""
    exit 1
fi

# Add all files except secrets
echo "📦 Adding files to Git..."
git add .
git add -f .streamlit/config.toml
# Note: secrets.toml is in .gitignore and won't be added

# Commit changes
echo "💾 Committing changes..."
git commit -m "Prepare for Streamlit Cloud deployment - MTN SmartAssist"

echo ""
echo "✅ Repository prepared for deployment!"
echo ""
echo "📋 Next Steps:"
echo "1. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/mtn-smartassist.git"
echo "   git push -u origin main"
echo ""
echo "2. Deploy on Streamlit Cloud:"
echo "   - Go to: https://share.streamlit.io/"
echo "   - Connect your GitHub repository"
echo "   - Set main file: app.py"
echo "   - Add your API keys in Secrets section"
echo ""
echo "3. Copy content from .streamlit/secrets.toml to Streamlit Cloud Secrets"
echo ""
echo "🎉 Your app will be live at: https://YOUR_USERNAME-mtn-smartassist-app-xyz.streamlit.app/"