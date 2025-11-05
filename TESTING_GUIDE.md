# MTN SmartAssist - Testing Guide

## Pre-Demo Testing Checklist

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with valid API key
- [ ] Internet connection available

### Data Verification
- [ ] `data/faqs.json` exists and contains FAQs
- [ ] `data/customer_data.csv` exists with 30 records
- [ ] `data/scraped_faqs.json` created (run scraper if missing)
- [ ] Churn model trained (`models/churn_model.pkl` exists)

### Application Launch
- [ ] Run `streamlit run app.py`
- [ ] Application opens in browser
- [ ] No error messages in terminal
- [ ] All tabs visible (Chat, Dashboard, Admin, About)

---

## Functional Testing

### 1. Chat Assistant Tests

#### Test Case 1.1: Basic Conversation
**Steps:**
1. Navigate to Chat Assistant tab
2. Type: "What data plans are available?"
3. Click Send

**Expected Result:**
- Response appears within 3 seconds
- Response mentions MTN data plans
- Intent shows "data_inquiry"
- Confidence > 0.7
- FAQ count > 0

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 1.2: Network Issue
**Steps:**
1. Type: "I'm having network problems"
2. Click Send

**Expected Result:**
- Empathetic response
- Troubleshooting steps provided
- Intent shows "network_complaint"
- Relevant FAQs displayed

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 1.3: Social Bundles (Scraped Content)
**Steps:**
1. Type: "Tell me about social bundles"
2. Click Send

**Expected Result:**
- Response includes scraped MTN content
- Mentions specific apps (WhatsApp, Facebook, etc.)
- Pricing information included
- Subscription instructions provided

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 1.4: Conversation Summary
**Steps:**
1. Have 3-4 message exchanges
2. Click "Get Summary" button

**Expected Result:**
- Summary generated within 5 seconds
- 2-3 sentence summary
- Key points captured
- Professional CRM-style language

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 1.5: Satisfaction Rating
**Steps:**
1. Select a star rating (e.g., ⭐⭐⭐⭐)
2. Check sidebar metrics

**Expected Result:**
- Success message appears
- Average satisfaction updates in sidebar
- Rating persists in session

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 1.6: Clear Chat
**Steps:**
1. Have some conversation history
2. Click "Clear Chat" button

**Expected Result:**
- All messages removed
- Chat area empty
- Conversation count resets
- No errors

**Status:** [ ] Pass [ ] Fail

---

### 2. Dashboard Tests

#### Test Case 2.1: Customer Overview
**Steps:**
1. Navigate to Dashboard tab
2. View overview metrics

**Expected Result:**
- Total Customers: 30
- Average Monthly Spend displayed
- Average Tenure displayed
- Total Complaints displayed
- All metrics are numbers (not errors)

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 2.2: Churn Prediction
**Steps:**
1. Click "Run Churn Prediction" button
2. Wait for completion

**Expected Result:**
- Success message appears
- High/Medium/Low risk counts displayed
- Pie chart shows risk distribution
- Histogram shows probability distribution
- High risk customers table populated
- Process completes in < 5 seconds

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 2.3: Risk Visualization
**Steps:**
1. After running prediction, examine charts

**Expected Result:**
- Pie chart has 3 segments (High/Medium/Low)
- Colors: Green (Low), Yellow (Medium), Red (High)
- Histogram shows distribution of probabilities
- Charts are interactive (hover shows values)

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 2.4: High Risk Customers
**Steps:**
1. Scroll to "High Risk Customers" table
2. Examine data

**Expected Result:**
- Table shows customers with risk_level = "High"
- Sorted by churn_probability (descending)
- Columns: customer_id, tenure_months, monthly_spend, complaints, churn_probability, risk_level
- Churn probability > 0.6 for all rows

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 2.5: Conversation Analytics
**Steps:**
1. After having some chat conversations
2. View conversation analytics section

**Expected Result:**
- Intent distribution bar chart displayed
- Average confidence metric shown
- Average response time shown
- Customer satisfaction shown (if rated)

**Status:** [ ] Pass [ ] Fail

---

### 3. Admin Panel Tests

#### Test Case 3.1: FAQ Scraping
**Steps:**
1. Navigate to Admin Panel → FAQ Management
2. Click "Scrape MTN Website FAQs"
3. Wait for completion

**Expected Result:**
- Success message: "Successfully scraped X FAQs!"
- X > 10 (at least 10 FAQs)
- Page refreshes
- New FAQs visible in list

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 3.2: View FAQs
**Steps:**
1. In FAQ Management tab
2. Expand FAQ items

**Expected Result:**
- Shows first 10 FAQs
- Each FAQ has question, answer, category
- Some FAQs show source: "mtn.ng"
- Expandable sections work properly

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 3.3: Model Training
**Steps:**
1. Navigate to Admin Panel → Model Training
2. Click "Train Model" button
3. Wait for completion

**Expected Result:**
- Success message appears
- AUC Score displayed (> 0.7)
- Target metric shown (> 0.7)
- Green checkmark if target met
- Feature importance chart displayed
- Classification report available in expander

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 3.4: Feature Importance
**Steps:**
1. After training, view feature importance chart

**Expected Result:**
- Horizontal bar chart displayed
- Features sorted by importance
- Top features: complaint_rate, call_minutes, data_per_month
- All bars visible and labeled

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 3.5: Data Upload
**Steps:**
1. Navigate to Admin Panel → Data Upload
2. Upload `data/customer_data.csv`
3. Review preview

**Expected Result:**
- File uploads successfully
- Preview shows first 5 rows
- Validation passes (green checkmark)
- "Save Data" button appears

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 3.6: Invalid Data Upload
**Steps:**
1. Create CSV with missing columns
2. Try to upload

**Expected Result:**
- Validation fails (red X)
- Error message lists missing columns
- "Save Data" button not shown
- No data saved

**Status:** [ ] Pass [ ] Fail

---

### 4. About Page Tests

#### Test Case 4.1: Documentation Display
**Steps:**
1. Navigate to About tab
2. Scroll through content

**Expected Result:**
- All sections visible
- Markdown formatted correctly
- No broken formatting
- Links work (if any)
- Code blocks formatted properly

**Status:** [ ] Pass [ ] Fail

---

### 5. Sidebar Tests

#### Test Case 5.1: Navigation
**Steps:**
1. Click each navigation option
2. Verify page changes

**Expected Result:**
- All 4 tabs accessible
- Page content changes correctly
- No errors on navigation
- Selected tab highlighted

**Status:** [ ] Pass [ ] Fail

---

#### Test Case 5.2: Quick Stats
**Steps:**
1. Have some conversations
2. Check sidebar metrics

**Expected Result:**
- Total Conversations increments
- Avg Response Time updates
- Avg Satisfaction shows (if rated)
- Metrics are accurate

**Status:** [ ] Pass [ ] Fail

---

## Performance Testing

### Response Time Tests

#### Test 5.1: Chat Response Time
**Target:** < 3 seconds

**Steps:**
1. Send 5 different messages
2. Record response time for each
3. Calculate average

**Results:**
- Message 1: _____ seconds
- Message 2: _____ seconds
- Message 3: _____ seconds
- Message 4: _____ seconds
- Message 5: _____ seconds
- **Average: _____ seconds**

**Status:** [ ] Pass (< 3s) [ ] Fail (≥ 3s)

---

#### Test 5.2: Churn Prediction Time
**Target:** < 5 seconds

**Steps:**
1. Run churn prediction
2. Record time from click to completion

**Result:** _____ seconds

**Status:** [ ] Pass (< 5s) [ ] Fail (≥ 5s)

---

#### Test 5.3: FAQ Scraping Time
**Target:** < 15 seconds

**Steps:**
1. Run FAQ scraper
2. Record time from click to completion

**Result:** _____ seconds

**Status:** [ ] Pass (< 15s) [ ] Fail (≥ 15s)

---

## Error Handling Tests

### Test 6.1: No API Key
**Steps:**
1. Remove API key from `.env`
2. Restart app
3. Try to chat

**Expected Result:**
- Error message: "AI service not configured"
- App doesn't crash
- Other features still work

**Status:** [ ] Pass [ ] Fail

---

### Test 6.2: Invalid API Key
**Steps:**
1. Set invalid API key in `.env`
2. Restart app
3. Try to chat

**Expected Result:**
- Error message about API authentication
- App doesn't crash
- Graceful error handling

**Status:** [ ] Pass [ ] Fail

---

### Test 6.3: Network Failure
**Steps:**
1. Disconnect internet
2. Try to scrape FAQs

**Expected Result:**
- Fallback FAQs used
- Error message shown
- App continues to function

**Status:** [ ] Pass [ ] Fail

---

### Test 6.4: Missing Data File
**Steps:**
1. Rename `data/customer_data.csv`
2. Navigate to Dashboard

**Expected Result:**
- Warning message shown
- App doesn't crash
- Suggests uploading data

**Status:** [ ] Pass [ ] Fail

---

## User Experience Tests

### Test 7.1: First-Time User Flow
**Steps:**
1. Fresh app launch
2. Follow natural user journey

**Expected Result:**
- Clear navigation
- Intuitive interface
- Helpful error messages
- No confusion

**Status:** [ ] Pass [ ] Fail

---

### Test 7.2: Mobile Responsiveness
**Steps:**
1. Resize browser window to mobile size
2. Test all features

**Expected Result:**
- Layout adjusts properly
- All buttons accessible
- Text readable
- Charts resize

**Status:** [ ] Pass [ ] Fail

---

## Integration Tests

### Test 8.1: End-to-End Chat Flow
**Steps:**
1. Start chat
2. Ask question
3. Get response
4. Rate conversation
5. Get summary
6. Check metrics

**Expected Result:**
- All steps complete successfully
- Data flows through all layers
- Metrics update correctly

**Status:** [ ] Pass [ ] Fail

---

### Test 8.2: End-to-End Churn Flow
**Steps:**
1. Upload customer data
2. Train model
3. Run prediction
4. View results
5. Export data (future)

**Expected Result:**
- All steps complete successfully
- Data persists correctly
- Visualizations accurate

**Status:** [ ] Pass [ ] Fail

---

## Demo Scenario Tests

### Scenario 1: Data Plan Inquiry
**User:** "I want to buy a data plan for social media"

**Expected Flow:**
1. Intent: data_inquiry or social_bundles
2. Response mentions social bundles
3. Pricing information included
4. Subscription code provided (*312#)
5. Relevant FAQs shown

**Status:** [ ] Pass [ ] Fail

---

### Scenario 2: Complaint Handling
**User:** "My network has been terrible for 3 days"

**Expected Flow:**
1. Intent: network_complaint
2. Empathetic response
3. Troubleshooting steps
4. Escalation option (dial 180)
5. Professional tone

**Status:** [ ] Pass [ ] Fail

---

### Scenario 3: Account Management
**User:** "How do I check my balance?"

**Expected Flow:**
1. Intent: general_inquiry
2. Clear instructions (*131#)
3. Alternative methods mentioned (MyMTN app)
4. Quick response

**Status:** [ ] Pass [ ] Fail

---

## Regression Tests

After any code changes, re-run:
- [ ] All chat tests (1.1-1.6)
- [ ] Churn prediction (2.2)
- [ ] Model training (3.3)
- [ ] Performance tests (5.1-5.3)

---

## Test Summary

**Date:** ___________  
**Tester:** ___________  
**Version:** ___________

**Results:**
- Total Tests: _____
- Passed: _____
- Failed: _____
- Skipped: _____

**Pass Rate:** _____%

**Critical Issues:**
1. ___________
2. ___________
3. ___________

**Recommendations:**
1. ___________
2. ___________
3. ___________

**Sign-off:** ___________

---

## Automated Testing (Future)

### Unit Tests
```python
# tests/test_chat_engine.py
def test_search_faqs():
    engine = ChatEngine()
    results = engine.search_faqs("data plan")
    assert len(results) > 0
    assert "data" in results[0]['answer'].lower()

# tests/test_churn_model.py
def test_churn_prediction():
    predictor = ChurnPredictor()
    df = pd.read_csv('data/customer_data.csv')
    results = predictor.predict(df)
    assert 'churn_probability' in results.columns
    assert results['churn_probability'].between(0, 1).all()
```

### Integration Tests
```python
# tests/test_integration.py
def test_end_to_end_chat():
    engine = ChatEngine()
    response = engine.generate_response("What data plans are available?")
    assert response['response'] is not None
    assert response['intent'] in engine.intents
    assert response['confidence'] > 0
```

### Run Tests
```bash
pytest tests/ -v
```

---

**Happy Testing! 🧪**
