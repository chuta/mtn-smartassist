# 🔄 How to Properly Restart the App

## The Issue
Streamlit caches environment variables and code. After making changes to `.env` or Python files, you need to fully restart the app.

## Quick Restart Steps

### Method 1: Terminal Restart (Recommended)

1. **Stop the app:**
   - Go to the terminal where Streamlit is running
   - Press `Ctrl + C` (or `Cmd + C` on Mac)
   - Wait for it to fully stop

2. **Restart the app:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

3. **Refresh browser:**
   - Go to http://localhost:8501
   - Hard refresh: `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)

### Method 2: Use the Run Script

```bash
# Stop current app (Ctrl+C)
bash run.sh
```

### Method 3: Streamlit Rerun (For Code Changes Only)

If you only changed Python code (not .env):
- Click "Rerun" in the top-right corner of the Streamlit app
- Or press `R` in the browser

**Note:** This does NOT reload .env changes!

## When to Restart

### Full Restart Required (Ctrl+C then restart):
- ✅ Changed `.env` file
- ✅ Changed API keys
- ✅ Added new Python files
- ✅ Changed imports
- ✅ App showing old behavior

### Rerun Sufficient (Click "Rerun"):
- ✅ Changed function logic
- ✅ Changed UI text
- ✅ Changed CSS styles
- ✅ Changed calculations

## Troubleshooting Restart Issues

### App Won't Stop
```bash
# Find the process
lsof -i :8501

# Kill it
kill -9 <PID>
```

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Changes Not Showing
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Hard refresh browser
Ctrl + Shift + R (or Cmd + Shift + R)
```

### Environment Variables Not Loading
```bash
# Verify .env file
cat .env

# Check if loaded
source venv/bin/activate
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:20])"
```

## Best Practices

### 1. Always Use Virtual Environment
```bash
source venv/bin/activate
```

### 2. Test After Changes
```bash
# Test API keys
python3 test_api_keys.py

# Test setup
python3 test_setup.py

# Then run app
streamlit run app.py
```

### 3. Clear Browser Cache
- Hard refresh after restart
- Or use incognito/private mode

### 4. Check Terminal Output
- Look for initialization messages
- Check for errors
- Verify "✅ AI Service initialized with OpenAI"

## Quick Checklist

Before restarting:
- [ ] Saved all file changes
- [ ] .env file has valid API key
- [ ] Virtual environment activated
- [ ] No syntax errors in code

After restarting:
- [ ] Terminal shows no errors
- [ ] Browser refreshed (hard refresh)
- [ ] App loads without errors
- [ ] Test a simple query

## Common Restart Scenarios

### Scenario 1: Changed API Key
```bash
# 1. Stop app (Ctrl+C)
# 2. Verify .env
cat .env | grep OPENAI_API_KEY
# 3. Test key
python3 test_api_keys.py
# 4. Restart
streamlit run app.py
```

### Scenario 2: Updated Code
```bash
# 1. Stop app (Ctrl+C)
# 2. Test code
python3 -m py_compile app.py
# 3. Restart
streamlit run app.py
```

### Scenario 3: UI Not Updating
```bash
# 1. Stop app (Ctrl+C)
# 2. Clear cache
rm -rf ~/.streamlit/cache
# 3. Restart
streamlit run app.py
# 4. Hard refresh browser (Ctrl+Shift+R)
```

## Verification

After restart, check:

1. **Terminal Output:**
   ```
   ✅ AI Service initialized with OpenAI
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

2. **Browser:**
   - App loads without errors
   - Chat interface visible
   - Input field working
   - Buttons clickable

3. **Test Query:**
   - Type: "Hello"
   - Should get AI response
   - No authentication errors

## Quick Commands Reference

```bash
# Stop app
Ctrl + C

# Activate venv
source venv/bin/activate

# Test setup
python3 test_setup.py

# Test API keys
python3 test_api_keys.py

# Run app
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502

# Clear cache
rm -rf ~/.streamlit/cache

# Hard refresh browser
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

---

**Remember:** Always do a full restart (Ctrl+C then restart) when changing .env or API keys!
