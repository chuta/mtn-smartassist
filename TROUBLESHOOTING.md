# 🔧 MTN SmartAssist - Troubleshooting Guide

## Common Issues & Solutions

### 1. TypeError: Client.__init__() got an unexpected keyword argument 'proxies'

**Error:**
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

**Cause:** OpenAI library version incompatibility

**Solution:**
```bash
source venv/bin/activate
pip install --upgrade openai anthropic
```

The app now uses flexible version requirements (openai>=1.0.0) to ensure compatibility.

---

### 2. "AI service not configured"

**Cause:** No API key in `.env` file

**Solution:**
1. Check if `.env` file exists
2. Add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart the application

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

---

### 3. "Module not found" errors

**Cause:** Dependencies not installed

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### 4. Virtual environment issues

**Cause:** Virtual environment not activated or corrupted

**Solution:**
```bash
# Remove old venv
rm -rf venv

# Create new venv
python3 -m venv venv

# Activate and install
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. Streamlit won't start

**Cause:** Port already in use or Streamlit not installed

**Solution:**
```bash
# Check if port 8501 is in use
lsof -i :8501

# Kill process if needed
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

---

### 6. Churn prediction fails

**Cause:** Model not trained or data file missing

**Solution:**
1. Check `data/customer_data.csv` exists
2. Go to Admin Panel → Model Training
3. Click "Train Model"
4. Wait for completion

---

### 7. FAQ scraping fails

**Cause:** Network issues or website structure changed

**Solution:**
- Check internet connection
- The app will automatically use fallback FAQs
- Scraped FAQs are optional, static FAQs still work

---

### 8. Slow responses

**Cause:** API rate limits or network latency

**Solution:**
- Check API usage limits
- Verify internet connection
- Consider upgrading API tier
- Response times vary by AI provider

---

### 9. Import errors after setup

**Cause:** Python path or virtual environment issues

**Solution:**
```bash
# Ensure you're in the project directory
cd /path/to/mtn-smartassist

# Activate venv
source venv/bin/activate

# Verify Python is from venv
which python3

# Should show: /path/to/mtn-smartassist/venv/bin/python3
```

---

### 10. Data validation errors

**Cause:** CSV file format incorrect

**Solution:**
Ensure CSV has these columns:
```
customer_id,tenure_months,monthly_spend,data_usage_gb,
call_minutes,complaints,last_recharge_days
```

Example:
```csv
C001,24,5000,15.5,450,2,3
```

---

## Testing Your Setup

### Quick Setup Test

Run the test script to verify everything:

```bash
source venv/bin/activate
python3 test_setup.py
```

This will check:
- ✅ Python version
- ✅ Dependencies installed
- ✅ API keys configured
- ✅ Data files present
- ✅ Services initialized
- ✅ Models loaded

### API Key Test

Test if your API keys actually work:

```bash
source venv/bin/activate
python3 test_api_keys.py
```

This will:
- ✅ Test OpenAI key with real API call
- ✅ Test Anthropic key with real API call
- ✅ Show which provider is working
- ✅ Provide specific error messages

---

## Platform-Specific Issues

### macOS

**Issue:** "externally-managed-environment" error

**Solution:**
Always use virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Issue:** Permission denied on scripts

**Solution:**
```bash
chmod +x setup.sh run.sh
```

### Linux

**Issue:** Python 3.8+ not available

**Solution:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv

# Use python3.10 instead of python3
python3.10 -m venv venv
```

### Windows

**Issue:** Scripts won't run

**Solution:**
Use PowerShell or Git Bash:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## API Key Issues

### OpenAI

**Issue:** Invalid API key or authentication error

**Check:**
- Key starts with `sk-proj-` or `sk-`
- No extra spaces or quotes
- Key is active in OpenAI dashboard
- Account has credits/billing set up

**Test:**
```bash
# Quick test
python3 test_api_keys.py

# Or manual test
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Common Issues:**
- Key expired → Get new key
- No credits → Add billing in OpenAI dashboard
- Rate limited → Wait or upgrade tier

### Anthropic

**Issue:** Invalid API key or authentication error (401)

**Check:**
- Key starts with `sk-ant-`
- No duplicate "ANTHROPIC_API_KEY=" prefix
- Key is active in Anthropic console
- Account has credits

**Test:**
```bash
python3 test_api_keys.py
```

**Important:** Use ONLY ONE provider at a time. Comment out the other in .env:
```bash
# Use OpenAI
OPENAI_API_KEY=sk-proj-...
# ANTHROPIC_API_KEY=sk-ant-...

# OR use Anthropic
# OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Performance Issues

### Slow Chat Responses

**Possible causes:**
1. Network latency
2. API rate limits
3. Large conversation history
4. Complex queries

**Solutions:**
- Clear chat history
- Check internet speed
- Verify API tier limits
- Simplify queries

### Dashboard Loading Slowly

**Possible causes:**
1. Large dataset
2. Complex visualizations
3. Multiple predictions running

**Solutions:**
- Use smaller datasets for testing
- Run predictions one at a time
- Close other browser tabs

---

## Data Issues

### Missing FAQs

**Check:**
1. `data/faqs.json` exists
2. `data/scraped_faqs.json` exists (optional)
3. Files are valid JSON

**Fix:**
```bash
# Re-scrape FAQs
source venv/bin/activate
python3 services/faq_scraper.py
```

### Missing Customer Data

**Check:**
1. `data/customer_data.csv` exists
2. File has correct format
3. No empty rows

**Fix:**
Use the provided sample data or upload new data via Admin Panel

---

## Browser Issues

### App not loading

**Solutions:**
1. Clear browser cache
2. Try incognito/private mode
3. Try different browser
4. Check console for errors (F12)

### Visualizations not showing

**Solutions:**
1. Enable JavaScript
2. Update browser
3. Check browser console for errors
4. Try different browser

---

## Getting Help

### Quick Checks

1. Run test script: `python3 test_setup.py`
2. Check error messages in terminal
3. Verify `.env` file configuration
4. Ensure virtual environment is activated
5. Check internet connection

### Documentation

- [QUICKSTART.md](QUICKSTART.md) - Setup guide
- [README.md](README.md) - Main documentation
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands
- [INDEX.md](INDEX.md) - All documentation

### Debug Mode

Enable debug output:
```bash
# In .env file
DEBUG_MODE=True
```

Then check terminal for detailed logs.

---

## Still Having Issues?

1. **Check error message** - Read the full error in terminal
2. **Search documentation** - Use INDEX.md to find relevant docs
3. **Run test script** - `python3 test_setup.py`
4. **Check versions** - Ensure Python 3.8+
5. **Fresh install** - Remove venv and reinstall

### Fresh Install Steps

```bash
# Backup your .env file
cp .env .env.backup

# Clean install
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Restore .env
cp .env.backup .env

# Test
python3 test_setup.py

# Run
streamlit run app.py
```

---

## Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `TypeError: Client.__init__()` | OpenAI version | `pip install --upgrade openai` |
| `ModuleNotFoundError` | Missing dependency | `pip install -r requirements.txt` |
| `FileNotFoundError` | Missing data file | Check data/ directory |
| `KeyError` | Invalid data format | Validate CSV columns |
| `ConnectionError` | Network issue | Check internet |
| `AuthenticationError` | Invalid API key | Check .env file |
| `RateLimitError` | API limit reached | Wait or upgrade tier |

---

**Last Updated:** April 11, 2025  
**Version:** 1.0
