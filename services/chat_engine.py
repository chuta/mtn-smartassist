import json
from typing import List, Dict, Optional
from services.ai_service import AIService

class ChatEngine:
    """Main chat engine for MTN SmartAssist"""
    
    def __init__(self, faq_file: str = "data/faqs.json", scraped_faq_file: str = "data/scraped_faqs.json"):
        self.ai_service = AIService()
        self.faqs = self._load_faqs(faq_file)
        self.scraped_faqs = self._load_faqs(scraped_faq_file)
        self.all_faqs = self.faqs + self.scraped_faqs
        
        self.intents = [
            "data_inquiry",
            "recharge_issue", 
            "network_complaint",
            "roaming_inquiry",
            "porting_request",
            "tariff_inquiry",
            "security_issue",
            "general_inquiry"
        ]
    
    def _load_faqs(self, filename: str) -> List[Dict]:
        """Load FAQs from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('faqs', [])
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading FAQs from {filename}: {e}")
            return []
    
    def search_faqs(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search FAQs based on keyword matching"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_faqs = []
        for faq in self.all_faqs:
            score = 0
            
            # Check keywords
            if 'keywords' in faq:
                keywords = [k.lower() for k in faq['keywords']]
                score += sum(2 for word in query_words if any(word in k for k in keywords))
            
            # Check question and answer
            question_lower = faq['question'].lower()
            answer_lower = faq['answer'].lower()
            
            score += sum(1 for word in query_words if word in question_lower)
            score += sum(0.5 for word in query_words if word in answer_lower)
            
            if score > 0:
                scored_faqs.append((score, faq))
        
        # Sort by score and return top_k
        scored_faqs.sort(reverse=True, key=lambda x: x[0])
        return [faq for score, faq in scored_faqs[:top_k]]
    
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> Dict:
        """Generate response to user message"""
        
        # Classify intent
        intent_result = self.ai_service.classify_intent(user_message, self.intents)
        
        # Search relevant FAQs
        relevant_faqs = self.search_faqs(user_message)
        
        # Build context for AI
        faq_context = "\n\n".join([
            f"FAQ: {faq['question']}\nAnswer: {faq['answer']}"
            for faq in relevant_faqs
        ]) if relevant_faqs else "No specific FAQs found."
        
        # Build system prompt
        system_prompt = """You are MTN SmartAssist, an AI customer service assistant for MTN Nigeria.

Your personality:
- Friendly, professional, and empathetic
- Use MTN brand voice: warm, helpful, and solution-oriented
- Keep responses concise but complete
- Always try to resolve issues or provide clear next steps

Guidelines:
- Use the FAQ context provided to give accurate information
- If you don't know something, direct customers to dial 180 or visit an MTN service center
- Be proactive in suggesting related services
- Show empathy for customer issues
- Use Nigerian English and local context"""

        # Build user prompt
        user_prompt = f"""Customer message: {user_message}

Detected intent: {intent_result.get('intent', 'unknown')}

Relevant FAQ context:
{faq_context}

Provide a helpful, friendly response that addresses the customer's needs. If the FAQ context is relevant, use it to inform your answer."""

        # Generate AI response
        ai_response = self.ai_service.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.7
        )
        
        return {
            "response": ai_response,
            "intent": intent_result.get('intent'),
            "confidence": intent_result.get('confidence', 0),
            "relevant_faqs": relevant_faqs,
            "faq_count": len(relevant_faqs)
        }
    
    def get_conversation_summary(self, conversation: List[Dict]) -> str:
        """Get summary of conversation"""
        return self.ai_service.summarize_conversation(conversation)
