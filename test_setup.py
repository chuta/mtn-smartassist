#!/usr/bin/env python3
"""Quick test to verify setup is working"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🧪 Testing MTN SmartAssist Setup...\n")

# Test 1: Check Python version
print("1️⃣ Python Version:")
print(f"   ✅ {sys.version}\n")

# Test 2: Check dependencies
print("2️⃣ Checking Dependencies:")
try:
    import streamlit
    print(f"   ✅ Streamlit {streamlit.__version__}")
except ImportError as e:
    print(f"   ❌ Streamlit: {e}")

try:
    import openai
    print(f"   ✅ OpenAI {openai.__version__}")
except ImportError as e:
    print(f"   ❌ OpenAI: {e}")

try:
    import anthropic
    print(f"   ✅ Anthropic {anthropic.__version__}")
except ImportError as e:
    print(f"   ❌ Anthropic: {e}")

try:
    import sklearn
    print(f"   ✅ Scikit-learn {sklearn.__version__}")
except ImportError as e:
    print(f"   ❌ Scikit-learn: {e}")

try:
    import pandas
    print(f"   ✅ Pandas {pandas.__version__}")
except ImportError as e:
    print(f"   ❌ Pandas: {e}")

print()

# Test 3: Check API keys
print("3️⃣ Checking API Keys:")
openai_key = os.getenv('OPENAI_API_KEY')
anthropic_key = os.getenv('ANTHROPIC_API_KEY')

if openai_key and openai_key.startswith('sk-'):
    print(f"   ✅ OpenAI API key configured")
else:
    print(f"   ⚠️  OpenAI API key not configured")

if anthropic_key and anthropic_key.startswith('sk-ant-'):
    print(f"   ✅ Anthropic API key configured")
else:
    print(f"   ⚠️  Anthropic API key not configured")

print()

# Test 4: Check data files
print("4️⃣ Checking Data Files:")
files_to_check = [
    'data/faqs.json',
    'data/customer_data.csv',
    'data/scraped_faqs.json'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} missing")

print()

# Test 5: Test AI Service initialization
print("5️⃣ Testing AI Service:")
try:
    from services.ai_service import AIService
    ai_service = AIService()
    if ai_service.is_available():
        print(f"   ✅ AI Service initialized ({ai_service.provider})")
    else:
        print(f"   ⚠️  AI Service not available (no API keys configured)")
except Exception as e:
    print(f"   ❌ AI Service error: {e}")

print()

# Test 6: Test Chat Engine
print("6️⃣ Testing Chat Engine:")
try:
    from services.chat_engine import ChatEngine
    chat_engine = ChatEngine()
    print(f"   ✅ Chat Engine initialized")
    print(f"   ✅ Total FAQs loaded: {len(chat_engine.all_faqs)}")
except Exception as e:
    print(f"   ❌ Chat Engine error: {e}")

print()

# Test 7: Test Churn Model
print("7️⃣ Testing Churn Model:")
try:
    from models.churn_model import ChurnPredictor
    predictor = ChurnPredictor()
    if predictor.load_model():
        print(f"   ✅ Churn model loaded")
    else:
        print(f"   ⚠️  Churn model not trained yet (run training in Admin Panel)")
except Exception as e:
    print(f"   ❌ Churn Model error: {e}")

print()

# Summary
print("=" * 50)
print("✅ Setup test complete!")
print("=" * 50)
print("\n🚀 Ready to run: streamlit run app.py")
