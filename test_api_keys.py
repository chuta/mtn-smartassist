#!/usr/bin/env python3
"""Test API keys to verify they work"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔑 Testing API Keys...\n")

# Test OpenAI
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    print(f"1️⃣ OpenAI API Key Found")
    print(f"   Key starts with: {openai_key[:10]}...")
    
    try:
        import openai
        client = openai.OpenAI(api_key=openai_key)
        
        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        
        print(f"   ✅ OpenAI API Key is VALID")
        print(f"   Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"   ❌ OpenAI API Key is INVALID")
        print(f"   Error: {str(e)}")
        print(f"\n   Please get a new key from: https://platform.openai.com/api-keys")
else:
    print(f"1️⃣ ❌ No OpenAI API Key found in .env")

print()

# Test Anthropic
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_key:
    print(f"2️⃣ Anthropic API Key Found")
    print(f"   Key starts with: {anthropic_key[:10]}...")
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        
        # Try a simple API call
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say 'Hello'"}]
        )
        
        print(f"   ✅ Anthropic API Key is VALID")
        print(f"   Response: {response.content[0].text}")
        
    except Exception as e:
        print(f"   ❌ Anthropic API Key is INVALID")
        print(f"   Error: {str(e)}")
        print(f"\n   Please get a new key from: https://console.anthropic.com/")
else:
    print(f"2️⃣ ⚠️  No Anthropic API Key found in .env (commented out)")

print()
print("=" * 60)
print("💡 Recommendation:")
print("   - Use ONLY ONE provider at a time")
print("   - Comment out the other provider's key in .env")
print("   - Restart the Streamlit app after changes")
print("=" * 60)
