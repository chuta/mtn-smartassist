from typing import Dict, List
import time

class MetricsTracker:
    """Track application metrics"""
    
    def __init__(self):
        self.conversation_metrics = []
        self.response_times = []
        self.satisfaction_scores = []
    
    def log_conversation(self, intent: str, confidence: float, response_time: float):
        """Log conversation metrics"""
        self.conversation_metrics.append({
            'intent': intent,
            'confidence': confidence,
            'timestamp': time.time()
        })
        self.response_times.append(response_time)
    
    def log_satisfaction(self, score: int):
        """Log customer satisfaction score (1-5)"""
        if 1 <= score <= 5:
            self.satisfaction_scores.append(score)
    
    def get_summary(self) -> Dict:
        """Get metrics summary"""
        if not self.conversation_metrics:
            return {
                'total_conversations': 0,
                'avg_response_time': 0,
                'avg_satisfaction': 0
            }
        
        return {
            'total_conversations': len(self.conversation_metrics),
            'avg_response_time': sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            'avg_confidence': sum(m['confidence'] for m in self.conversation_metrics) / len(self.conversation_metrics),
            'avg_satisfaction': sum(self.satisfaction_scores) / len(self.satisfaction_scores) if self.satisfaction_scores else 0,
            'intent_distribution': self._get_intent_distribution()
        }
    
    def _get_intent_distribution(self) -> Dict:
        """Get distribution of intents"""
        intents = [m['intent'] for m in self.conversation_metrics]
        distribution = {}
        for intent in intents:
            distribution[intent] = distribution.get(intent, 0) + 1
        return distribution
