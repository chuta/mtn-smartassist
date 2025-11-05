#!/bin/bash

# MTN SmartAssist Setup Script
echo "🚀 Setting up MTN SmartAssist..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Scrape FAQs
echo ""
echo "🌐 Scraping MTN FAQs..."
python3 services/faq_scraper.py

# Train churn model
echo ""
echo "🎓 Training churn prediction model..."
python3 models/churn_model.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env and add your API key (OpenAI or Anthropic)"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run app.py"
echo ""
echo "🎉 Happy coding!"
