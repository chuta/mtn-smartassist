import requests
from bs4 import BeautifulSoup
import json
import re

class FAQScraper:
    """Scrapes FAQs from MTN Nigeria website"""
    
    def __init__(self):
        self.base_url = "https://www.mtn.ng"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_social_bundles_faq(self, url="https://www.mtn.ng/helppersonal/social-bundles/"):
        """Scrape FAQs from MTN social bundles page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            faqs = []
            
            # Look for FAQ sections - adjust selectors based on actual page structure
            faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'faq|question|accordion', re.I))
            
            # Try multiple patterns to extract FAQs
            for section in faq_sections:
                questions = section.find_all(['h3', 'h4', 'h5', 'strong', 'b'])
                for q in questions:
                    question_text = q.get_text(strip=True)
                    if len(question_text) > 10:  # Filter out short non-questions
                        # Find answer (next sibling or parent's next sibling)
                        answer_elem = q.find_next(['p', 'div', 'span'])
                        answer_text = answer_elem.get_text(strip=True) if answer_elem else ""
                        
                        if answer_text and len(answer_text) > 20:
                            faqs.append({
                                "question": question_text,
                                "answer": answer_text,
                                "category": "social_bundles",
                                "source": "mtn.ng"
                            })
            
            # Also extract general content about social bundles
            content_divs = soup.find_all(['div', 'section'], class_=re.compile(r'content|main|body', re.I))
            for div in content_divs:
                paragraphs = div.find_all('p')
                for i, p in enumerate(paragraphs):
                    text = p.get_text(strip=True)
                    if 'social' in text.lower() and 'bundle' in text.lower() and len(text) > 50:
                        faqs.append({
                            "question": f"Information about MTN Social Bundles {i+1}",
                            "answer": text,
                            "category": "social_bundles",
                            "source": "mtn.ng"
                        })
            
            # Remove duplicates
            unique_faqs = []
            seen = set()
            for faq in faqs:
                key = faq['question'][:50]  # Use first 50 chars as key
                if key not in seen:
                    seen.add(key)
                    unique_faqs.append(faq)
            
            return unique_faqs
            
        except Exception as e:
            print(f"Error scraping FAQs: {e}")
            # Return fallback social bundles FAQs
            return self._get_fallback_social_bundles_faqs()
    
    def _get_fallback_social_bundles_faqs(self):
        """Fallback FAQs if scraping fails"""
        return [
            {
                "question": "What are MTN Social Bundles?",
                "answer": "MTN Social Bundles are special data packages designed specifically for social media platforms like WhatsApp, Facebook, Instagram, Twitter, and TikTok. These bundles offer affordable data rates for your favorite social apps.",
                "category": "social_bundles",
                "source": "fallback"
            },
            {
                "question": "How do I subscribe to Social Bundles?",
                "answer": "To subscribe to MTN Social Bundles, dial *312# and select your preferred social media bundle. You can also subscribe via the MyMTN app or by visiting mtn.ng.",
                "category": "social_bundles",
                "source": "fallback"
            },
            {
                "question": "What social media platforms are covered?",
                "answer": "MTN Social Bundles cover popular platforms including WhatsApp, Facebook, Instagram, Twitter, TikTok, and Snapchat. Different bundle tiers may include different combinations of these platforms.",
                "category": "social_bundles",
                "source": "fallback"
            },
            {
                "question": "How long do Social Bundles last?",
                "answer": "MTN Social Bundles typically have validity periods ranging from daily (24 hours), weekly (7 days), to monthly (30 days) depending on the bundle you purchase.",
                "category": "social_bundles",
                "source": "fallback"
            },
            {
                "question": "Can I use Social Bundles for other apps?",
                "answer": "No, Social Bundles are exclusively for the specified social media platforms. For general internet browsing, you'll need to purchase regular data bundles.",
                "category": "social_bundles",
                "source": "fallback"
            }
        ]
    
    def save_to_file(self, faqs, filename="data/scraped_faqs.json"):
        """Save scraped FAQs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"faqs": faqs, "source": "mtn.ng", "scraped": True}, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving FAQs: {e}")
            return False

if __name__ == "__main__":
    scraper = FAQScraper()
    print("Scraping MTN Social Bundles FAQs...")
    faqs = scraper.scrape_social_bundles_faq()
    print(f"Scraped {len(faqs)} FAQs")
    scraper.save_to_file(faqs)
    print("FAQs saved to data/scraped_faqs.json")
