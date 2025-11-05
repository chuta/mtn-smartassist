# MTN SmartAssist - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key (choose one):

**Option A: OpenAI**
```
OPENAI_API_KEY=sk-your-key-here
```

**Option B: Anthropic Claude**
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

> **Don't have an API key?** 
> - OpenAI: https://platform.openai.com/api-keys
> - Anthropic: https://console.anthropic.com/

### Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 4: Initial Setup

1. **Navigate to Admin Panel** → Model Training
2. Click **"Train Model"** to train the churn predictor
3. Wait for training to complete (~10 seconds)
4. Navigate to **Admin Panel** → FAQ Management
5. Click **"Scrape MTN Website FAQs"** to fetch latest FAQs

### Step 5: Start Chatting!

1. Go to **Chat Assistant** tab
2. Try these example queries:
   - "What data plans are available?"
   - "How do I check my balance?"
   - "Tell me about social bundles"
   - "I'm having network issues"

---

## 📋 Troubleshooting

### Issue: "AI service not configured"
**Solution:** Make sure you've added a valid API key to `.env` file

### Issue: "Module not found" errors
**Solution:** Run `pip install -r requirements.txt` again

### Issue: Churn prediction fails
**Solution:** Ensure `data/customer_data.csv` exists and is properly formatted

### Issue: FAQ scraping fails
**Solution:** Check internet connection. The app will use fallback FAQs automatically.

---

## 🎯 Quick Demo Flow

1. **Chat** → Ask 2-3 questions → Get Summary
2. **Dashboard** → Run Churn Prediction → View Analytics
3. **Admin Panel** → Scrape FAQs → Train Model

---

## 📊 Sample Queries for Demo

### Data Plans
- "What data plans do you have?"
- "How much is 1GB?"
- "Tell me about monthly bundles"

### Technical Support
- "My network is not working"
- "How do I fix poor signal?"
- "I can't connect to the internet"

### Account Management
- "How do I recharge?"
- "Check my balance"
- "I lost my SIM card"

### Social Bundles
- "What are social bundles?"
- "How do I subscribe to WhatsApp bundle?"
- "Tell me about Facebook data"

---

## 🔧 Advanced Configuration

### Change AI Model

Edit `services/ai_service.py`:
- OpenAI: Change `model="gpt-3.5-turbo"` to `"gpt-4"`
- Claude: Change `model="claude-3-haiku-20240307"` to `"claude-3-sonnet-20240229"`

### Adjust Response Style

Edit `services/chat_engine.py` → `system_prompt` to customize:
- Tone (formal/casual)
- Response length
- Brand voice

### Add Custom FAQs

Edit `data/faqs.json` and add:
```json
{
  "id": 99,
  "question": "Your question here",
  "answer": "Your answer here",
  "category": "category_name",
  "keywords": ["keyword1", "keyword2"]
}
```

---

## 📱 For Training Facilitators

### Pre-Demo Checklist
- [ ] Test all features work
- [ ] Clear chat history
- [ ] Reset metrics
- [ ] Verify API keys are valid
- [ ] Check internet connection
- [ ] Have backup demo ready

### During Training
- Show live coding (optional)
- Explain architecture
- Discuss AI ethics
- Demonstrate metrics
- Encourage hands-on practice

### Post-Training
- Share repository
- Provide API key guidance
- Collect feedback
- Answer questions

---

## 🆘 Need Help?

- **Documentation:** See README.md
- **Demo Script:** See DEMO_SCRIPT.md
- **Issues:** Check error messages in terminal
- **API Limits:** Free tier has rate limits, upgrade if needed

---

## 🎓 Learning Resources

### AI/ML Concepts
- Intent Classification
- Gradient Boosting
- Feature Engineering
- Model Evaluation (AUC, ROC)

### Tools & Frameworks
- Streamlit Documentation: https://docs.streamlit.io
- Scikit-learn: https://scikit-learn.org
- OpenAI API: https://platform.openai.com/docs

### MTN Context
- MTN Nigeria: https://www.mtn.ng
- Customer Service Best Practices
- Telecom Industry Metrics

---

**Ready to go! Start with `streamlit run app.py` and explore! 🚀**
