import os
from typing import Optional, Dict, List
import json

class AIService:
    """Handles AI provider integration (OpenAI/Claude)"""
    
    def __init__(self):
        # Try Streamlit secrets first (for cloud deployment), then environment variables (for local)
        try:
            import streamlit as st
            self.openai_key = st.secrets.get("OPENAI_API_KEY", "")
            self.anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except:
            # Fallback to environment variables for local development
            from dotenv import load_dotenv
            load_dotenv()
            self.openai_key = os.getenv('OPENAI_API_KEY')
            self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.provider = None
        self.client = None
        
        # Initialize available provider - try OpenAI first
        if self.openai_key and self.openai_key.startswith('sk-'):
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.openai_key)
                self.provider = 'openai'
                print(f"✅ AI Service initialized with OpenAI")
            except Exception as e:
                print(f"⚠️ OpenAI initialization failed: {e}")
                self.client = None
                self.provider = None
        
        # Try Anthropic only if OpenAI failed
        if not self.provider and self.anthropic_key and self.anthropic_key.startswith('sk-ant-'):
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.anthropic_key)
                self.provider = 'anthropic'
                print(f"✅ AI Service initialized with Anthropic")
            except Exception as e:
                print(f"⚠️ Anthropic initialization failed: {e}")
                self.client = None
                self.provider = None
        
        if not self.provider:
            print("⚠️ No AI provider configured. Please add a valid API key to .env file.")
    
    def is_available(self) -> bool:
        """Check if AI service is configured"""
        return self.provider is not None
    
    def generate_response(self, prompt: str, system_prompt: str = "", max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate AI response"""
        if not self.is_available():
            return "⚠️ AI service not configured. Please add a valid API key to .env file.\n\nGet API keys:\n- OpenAI: https://platform.openai.com/api-keys\n- Anthropic: https://console.anthropic.com/"
        
        try:
            if self.provider == 'openai':
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            
            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt if system_prompt else "You are a helpful assistant.",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
        
        except Exception as e:
            error_msg = str(e)
            if "authentication" in error_msg.lower() or "401" in error_msg:
                return f"❌ Authentication Error: Your API key is invalid or expired.\n\nPlease:\n1. Check your API key in .env file\n2. Ensure it's active in your provider dashboard\n3. Get a new key if needed:\n   - OpenAI: https://platform.openai.com/api-keys\n   - Anthropic: https://console.anthropic.com/\n\nError details: {error_msg}"
            elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                return f"⚠️ Rate Limit: You've exceeded your API usage limit.\n\nPlease:\n1. Wait a few minutes and try again\n2. Check your usage at your provider dashboard\n3. Consider upgrading your API tier\n\nError details: {error_msg}"
            else:
                return f"❌ Error: {error_msg}\n\nPlease check:\n1. Your internet connection\n2. API key is valid\n3. Service is not down"
    
    def classify_intent(self, user_message: str, intents: List[str]) -> Dict:
        """Classify user intent"""
        prompt = f"""Classify the following customer message into one of these intents: {', '.join(intents)}

Customer message: "{user_message}"

Respond with JSON format:
{{"intent": "intent_name", "confidence": 0.95, "entities": {{}}"}}"""
        
        system_prompt = "You are an intent classification system. Always respond with valid JSON only."
        
        response = self.generate_response(prompt, system_prompt, max_tokens=150, temperature=0.3)
        
        try:
            return json.loads(response)
        except:
            # Fallback intent detection
            message_lower = user_message.lower()
            if any(word in message_lower for word in ['data', 'bundle', 'plan', 'gb', 'mb']):
                return {"intent": "data_inquiry", "confidence": 0.8, "entities": {}}
            elif any(word in message_lower for word in ['recharge', 'airtime', 'top up']):
                return {"intent": "recharge_issue", "confidence": 0.8, "entities": {}}
            elif any(word in message_lower for word in ['network', 'signal', 'connection']):
                return {"intent": "network_complaint", "confidence": 0.8, "entities": {}}
            else:
                return {"intent": "general_inquiry", "confidence": 0.6, "entities": {}}
    
    def summarize_conversation(self, conversation: List[Dict]) -> str:
        """Summarize a conversation for CRM notes"""
        conv_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])
        
        prompt = f"""Summarize this customer service conversation in 2-3 concise sentences for CRM notes:

{conv_text}

Summary:"""
        
        system_prompt = "You are a customer service analyst. Create brief, professional summaries."
        
        return self.generate_response(prompt, system_prompt, max_tokens=150, temperature=0.5)
