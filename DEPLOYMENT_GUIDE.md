# 🚀 MTN SmartAssist - Deployment Guide

## Why Not Netlify?

**Netlify** only hosts static websites (HTML, CSS, JavaScript). Our MTN SmartAssist is a **Python Streamlit application** that needs a server to run Python code, so Netlify won't work.

## ✅ Best Hosting Options

### 🥇 **Option 1: Streamlit Community Cloud (RECOMMENDED)**

**Perfect for training demos!**
- ✅ **FREE** hosting
- ✅ **Easy setup** (5 minutes)
- ✅ **Automatic updates** from GitHub
- ✅ **Public sharing** with direct links
- ✅ **No credit card** required

---

## 🎯 **Streamlit Cloud Deployment (Step-by-Step)**

### **Prerequisites:**
- GitHub account
- MTN SmartAssist code in a GitHub repository

### **Step 1: Prepare Repository**

1. **Create GitHub repository:**
   ```bash
   # If not already done
   git init
   git add .
   git commit -m "Initial commit - MTN SmartAssist"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/mtn-smartassist.git
   git push -u origin main
   ```

2. **Create secrets file for API keys:**
   ```bash
   # Create .streamlit/secrets.toml (instead of .env)
   mkdir -p .streamlit
   ```

### **Step 2: Configure Secrets**

Create `.streamlit/secrets.toml`:
```toml
# .streamlit/secrets.toml
[secrets]
OPENAI_API_KEY = "sk-proj-your-key-here"
# ANTHROPIC_API_KEY = "sk-ant-your-key-here"

APP_TITLE = "MTN SmartAssist"
APP_ICON = "📱"
DEBUG_MODE = false
CHURN_MODEL_THRESHOLD = 0.6
MAX_RESPONSE_TOKENS = 500
TEMPERATURE = 0.7
```

### **Step 3: Update Code for Streamlit Cloud**

Update `services/ai_service.py` to use Streamlit secrets:

```python
import streamlit as st

class AIService:
    def __init__(self):
        # Try Streamlit secrets first, then environment variables
        try:
            self.openai_key = st.secrets["OPENAI_API_KEY"]
            self.anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            self.openai_key = os.getenv('OPENAI_API_KEY')
            self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Rest of initialization code...
```

### **Step 4: Deploy to Streamlit Cloud**

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub

2. **Create new app:**
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/mtn-smartassist`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Add secrets:**
   - In app settings → "Secrets"
   - Paste your `.streamlit/secrets.toml` content
   - Save

### **Step 5: Share Your App**

Your app will be available at:
```
https://YOUR_USERNAME-mtn-smartassist-app-xyz123.streamlit.app/
```

**Share this link with training participants!**

---

## 🔧 **Alternative: Heroku Deployment**

### **Step 1: Prepare for Heroku**

1. **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.11.0
   ```

3. **Update `requirements.txt`:**
   ```
   streamlit==1.31.0
   openai>=1.0.0
   anthropic>=0.18.0
   scikit-learn>=1.4.0
   pandas>=2.0.0
   numpy>=1.24.0
   requests>=2.31.0
   beautifulsoup4>=4.12.0
   python-dotenv>=1.0.0
   plotly>=5.18.0
   joblib>=1.3.0
   ```

### **Step 2: Deploy to Heroku**

1. **Install Heroku CLI**
2. **Login and create app:**
   ```bash
   heroku login
   heroku create mtn-smartassist-demo
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY="sk-proj-your-key-here"
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

---

## 🚀 **Quick Deployment (Streamlit Cloud)**

### **For Immediate Demo:**

1. **Fork the repository** (if you don't own it)
2. **Go to** https://share.streamlit.io/
3. **Connect GitHub** and select repository
4. **Add API key** in secrets
5. **Deploy!**

**Result:** Public URL for training participants in 5 minutes!

---

## 📋 **Deployment Checklist**

### **Before Deployment:**
- [ ] Code tested locally
- [ ] API keys working
- [ ] All dependencies in requirements.txt
- [ ] No sensitive data in code
- [ ] .gitignore includes .env

### **For Streamlit Cloud:**
- [ ] GitHub repository created
- [ ] .streamlit/secrets.toml configured
- [ ] Code updated to use st.secrets
- [ ] Repository is public (for free tier)

### **After Deployment:**
- [ ] App loads without errors
- [ ] Chat functionality works
- [ ] Churn prediction works
- [ ] All features accessible
- [ ] Share URL with participants

---

## 🔒 **Security Considerations**

### **API Keys:**
- ✅ Use Streamlit secrets (not .env in repo)
- ✅ Never commit API keys to GitHub
- ✅ Use environment variables in production

### **Repository:**
- ✅ Make repository public for free Streamlit hosting
- ✅ Ensure no sensitive data in code
- ✅ Use .gitignore for local files

---

## 🌐 **Custom Domain (Optional)**

### **For Professional URLs:**

1. **Streamlit Cloud Pro:** Custom domains available
2. **Heroku:** Add custom domain in settings
3. **Cloudflare:** Use as CDN/proxy

---

## 📊 **Monitoring & Analytics**

### **Streamlit Cloud:**
- Built-in usage analytics
- Error monitoring
- Performance metrics

### **Additional Monitoring:**
- Google Analytics (add to app)
- User feedback collection
- Usage tracking

---

## 🎯 **Training Deployment Strategy**

### **Recommended Approach:**

1. **Deploy to Streamlit Cloud** (free, easy)
2. **Share public URL** with participants
3. **Provide backup local setup** instructions
4. **Monitor usage** during training

### **Participant Access:**
```
Training URL: https://your-app.streamlit.app/
Backup: Local setup instructions
Support: QUICK_FIX.md guide
```

---

## 🚨 **Common Deployment Issues**

### **Issue: App won't start**
**Solution:** Check requirements.txt and Python version

### **Issue: API key not working**
**Solution:** Verify secrets configuration

### **Issue: Import errors**
**Solution:** Ensure all files in repository

### **Issue: Slow loading**
**Solution:** Optimize imports and caching

---

## 📞 **Deployment Support**

### **Streamlit Cloud:**
- Documentation: https://docs.streamlit.io/streamlit-community-cloud
- Community: https://discuss.streamlit.io/

### **Heroku:**
- Documentation: https://devcenter.heroku.com/
- Support: Heroku help center

---

## 🎉 **Next Steps**

1. **Choose deployment platform** (Streamlit Cloud recommended)
2. **Follow step-by-step guide** above
3. **Test deployed app** thoroughly
4. **Share URL** with training participants
5. **Monitor usage** during training

---

**Deployment Time: 5-15 minutes**  
**Cost: FREE (with Streamlit Cloud)**  
**Result: Public URL for training demos!** 🚀