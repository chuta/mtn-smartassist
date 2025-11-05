# 🚑 Quick Fix Guide - Common Errors

## ❌ Error: "authentication_error" or "invalid x-api-key"

**What you see:**
```
Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}}
```

**Quick Fix:**

1. **Stop the Streamlit app** (Ctrl+C in terminal)

2. **Test your API keys:**
   ```bash
   source venv/bin/activate
   python3 test_api_keys.py
   ```

3. **If OpenAI key is valid:**
   - Make sure Anthropic key is commented out in `.env`
   - Your `.env` should look like:
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   # ANTHROPIC_API_KEY=sk-ant-...
   ```

4. **If OpenAI key is invalid:**
   - Get a new key from https://platform.openai.com/api-keys
   - Replace in `.env` file
   - Make sure you have billing set up

5. **Restart the app:**
   ```bash
   streamlit run app.py
   ```

---

## ❌ Error: "TypeError: Client.__init__()"

**Quick Fix:**
```bash
source venv/bin/activate
pip install --upgrade openai anthropic
streamlit run app.py
```

---

## ❌ Error: "AI service not configured"

**Quick Fix:**

1. Check `.env` file exists:
   ```bash
   ls -la .env
   ```

2. If missing, create it:
   ```bash
   cp .env.example .env
   ```

3. Add your API key to `.env`:
   ```bash
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```

4. Restart app

---

## ❌ Error: "Module not found"

**Quick Fix:**
```bash
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## ❌ Error: Rate limit exceeded

**Quick Fix:**

1. **Wait 1 minute** - Rate limits reset quickly
2. **Check usage** at https://platform.openai.com/usage
3. **Upgrade tier** if needed
4. **Use fewer requests** - Clear chat history

---

## ❌ Chat responses are slow

**Quick Fix:**

1. **Check internet connection**
2. **Clear chat history** (click "Clear Chat" button)
3. **Use shorter queries**
4. **Check API status:**
   - OpenAI: https://status.openai.com
   - Anthropic: https://status.anthropic.com

---

## ❌ Churn prediction not working

**Quick Fix:**

1. Go to **Admin Panel** → **Model Training**
2. Click **"Train Model"**
3. Wait 10 seconds
4. Go back to **Dashboard**
5. Click **"Run Churn Prediction"**

---

## ❌ FAQs not loading

**Quick Fix:**

1. Check files exist:
   ```bash
   ls -la data/faqs.json data/scraped_faqs.json
   ```

2. If missing, scrape new FAQs:
   ```bash
   source venv/bin/activate
   python3 services/faq_scraper.py
   ```

3. Restart app

---

## ❌ App won't start

**Quick Fix:**

1. **Check port 8501:**
   ```bash
   lsof -i :8501
   ```

2. **Kill if needed:**
   ```bash
   kill -9 <PID>
   ```

3. **Or use different port:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

## ❌ Virtual environment issues

**Quick Fix - Fresh Install:**

```bash
# Backup .env
cp .env .env.backup

# Clean install
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Restore .env
cp .env.backup .env

# Test
python3 test_api_keys.py

# Run
streamlit run app.py
```

---

## 🆘 Still Not Working?

### Step 1: Run Diagnostics
```bash
source venv/bin/activate
python3 test_setup.py
python3 test_api_keys.py
```

### Step 2: Check Error Messages
- Read the FULL error in terminal
- Look for keywords: "authentication", "rate_limit", "connection"

### Step 3: Verify Configuration
```bash
# Check .env file
cat .env

# Should show:
# OPENAI_API_KEY=sk-proj-...
# (Anthropic should be commented out)
```

### Step 4: Test API Key Manually
```bash
# Test OpenAI key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Should return list of models, not error
```

### Step 5: Fresh Start
```bash
# Stop app (Ctrl+C)
# Clear browser cache
# Restart app
streamlit run app.py
```

---

## 📞 Need More Help?

- **Full Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Setup Guide:** [QUICKSTART.md](QUICKSTART.md)
- **Documentation:** [INDEX.md](INDEX.md)

---

## ✅ Prevention Tips

1. **Use ONE provider** - Comment out the other in `.env`
2. **Test keys first** - Run `python3 test_api_keys.py`
3. **Check billing** - Ensure account has credits
4. **Monitor usage** - Check provider dashboard
5. **Keep keys secure** - Never commit `.env` to git

---

**Last Updated:** April 11, 2025
