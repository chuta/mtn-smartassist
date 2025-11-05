import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from services.chat_engine import ChatEngine
from services.faq_scraper import FAQScraper
from models.churn_model import ChurnPredictor
from utils.metrics import MetricsTracker
from utils.data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="MTN SmartAssist",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FFCC00;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FFCC00 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #1a1a1a;
        font-size: 1rem;
        line-height: 1.5;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
        border-left: 4px solid #2196F3;
        color: #000000;
        font-weight: 500;
    }
    .assistant-message {
        background-color: #fff9e6;
        border-left: 4px solid #FFCC00;
        color: #000000;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FFCC00;
    }
    
    /* Fix Streamlit input text color */
    .stTextInput > div > div > input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #FFCC00 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666666 !important;
    }
    
    /* Fix text area color */
    .stTextArea > div > div > textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #FFCC00 !important;
    }
    
    /* Fix selectbox text */
    .stSelectbox > div > div > select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Ensure all text is readable */
    p, span, div, label {
        color: #1a1a1a;
    }
    
    /* Fix expander text */
    .streamlit-expanderHeader {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
    }
    
    /* Fix metric labels and values */
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    
    /* Fix markdown text */
    .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Improve button contrast */
    .stButton > button {
        background-color: #FFCC00 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        background-color: #FFA500 !important;
        color: #000000 !important;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background-color: #2196F3 !important;
        color: #ffffff !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #1976D2 !important;
    }
    
    /* Fix sidebar text colors */
    .css-1d391kg, .css-1v0mbdj, .css-16huue1 {
        color: #ffffff !important;
    }
    
    /* Fix sidebar navigation radio buttons */
    .stRadio > label {
        color: #ffffff !important;
    }
    
    .stRadio > div {
        color: #ffffff !important;
    }
    
    .stRadio > div > label {
        color: #ffffff !important;
    }
    
    .stRadio > div > label > div {
        color: #ffffff !important;
    }
    
    /* Fix sidebar headers */
    .css-1v0mbdj h3, .css-1v0mbdj h2, .css-1v0mbdj h1 {
        color: #ffffff !important;
    }
    
    /* Fix sidebar markdown text */
    .css-1v0mbdj p, .css-1v0mbdj span, .css-1v0mbdj div {
        color: #ffffff !important;
    }
    
    /* Fix all sidebar content */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    
    /* Fix main content area text */
    .main .block-container {
        background-color: #ffffff;
    }
    
    .main .block-container * {
        color: #000000;
    }
    
    /* Fix expander content */
    .streamlit-expanderContent {
        background-color: #f8f9fa !important;
        color: #000000 !important;
    }
    
    .streamlit-expanderContent * {
        color: #000000 !important;
    }
    
    /* Fix response details section */
    [data-testid="stExpander"] {
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    [data-testid="stExpander"] * {
        color: #000000 !important;
    }
    
    /* Fix metric labels in expander */
    [data-testid="stExpander"] [data-testid="stMetricLabel"],
    [data-testid="stExpander"] [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    
    /* Fix selectbox in main area */
    .main .stSelectbox label {
        color: #000000 !important;
    }
    
    /* Fix all labels in main content */
    .main label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Fix headers in main content */
    .main h1, .main h2, .main h3, .main h4 {
        color: #000000 !important;
    }
    
    /* Fix info/warning/success boxes */
    .stAlert {
        color: #000000 !important;
    }
    
    /* Fix dataframe text */
    .dataframe {
        color: #000000 !important;
    }
    
    .dataframe th {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }
    
    .dataframe td {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'metrics_tracker' not in st.session_state:
    st.session_state.metrics_tracker = MetricsTracker()
if 'chat_engine' not in st.session_state:
    st.session_state.chat_engine = ChatEngine()
if 'churn_predictor' not in st.session_state:
    st.session_state.churn_predictor = ChurnPredictor()
    # Try to load existing model
    st.session_state.churn_predictor.load_model()

# Sidebar
with st.sidebar:
    # Use local MTN logo
    try:
        st.image("New-mtn-logo.jpg", width=150)
    except:
        # Fallback to online logo if local file not found
        st.image("https://www.mtn.ng/wp-content/uploads/2021/03/mtn-logo.png", width=150)
    st.title("MTN SmartAssist")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["💬 Chat Assistant", "📊 Dashboard", "🔧 Admin Panel", "ℹ️ About"]
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    metrics = st.session_state.metrics_tracker.get_summary()
    st.metric("Total Conversations", metrics['total_conversations'])
    st.metric("Avg Response Time", f"{metrics['avg_response_time']:.2f}s")
    if metrics['avg_satisfaction'] > 0:
        st.metric("Avg Satisfaction", f"{metrics['avg_satisfaction']:.1f}/5")

# Main content
if page == "💬 Chat Assistant":
    st.markdown('<h1 class="main-header">MTN SmartAssist Chat</h1>', unsafe_allow_html=True)
    st.markdown("Ask me anything about MTN services, data plans, recharge, or network issues!")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message assistant-message">
                    <strong>🤖 MTN SmartAssist:</strong><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
                
                # Show intent and confidence if available
                if 'metadata' in message:
                    with st.expander("📊 Response Details"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Intent", message['metadata'].get('intent', 'N/A'))
                        col2.metric("Confidence", f"{message['metadata'].get('confidence', 0):.2%}")
                        col3.metric("FAQs Used", message['metadata'].get('faq_count', 0))
    
    # Chat input with form for Enter key support
    st.markdown("---")
    st.markdown('<h3 style="color: #000000; font-weight: 600;">💬 Your Message</h3>', unsafe_allow_html=True)
    
    # Use form to enable Enter key submission
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message here...", 
                placeholder="Ask me about data plans, recharge, network issues... (Press Enter to send)",
                label_visibility="collapsed",
                key="message_input"
            )
        
        with col2:
            send_button = st.form_submit_button("Send 📤", use_container_width=True, type="primary")
    
    # Process message when form is submitted (Enter key or Send button)
    if send_button and user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Generate response
        start_time = time.time()
        with st.spinner("Thinking..."):
            response_data = st.session_state.chat_engine.generate_response(
                user_input,
                st.session_state.chat_history
            )
        response_time = time.time() - start_time
        
        # Add assistant message
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response_data['response'],
            'timestamp': datetime.now(),
            'metadata': response_data
        })
        
        # Log metrics
        st.session_state.metrics_tracker.log_conversation(
            response_data['intent'],
            response_data['confidence'],
            response_time
        )
        
        st.rerun()
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("📝 Get Summary") and len(st.session_state.chat_history) > 0:
            with st.spinner("Generating summary..."):
                summary = st.session_state.chat_engine.get_conversation_summary(
                    st.session_state.chat_history
                )
            st.success("Conversation Summary:")
            st.info(summary)
    
    with col3:
        satisfaction = st.selectbox("Rate this chat:", ["", "⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
        if satisfaction:
            score = len(satisfaction)
            st.session_state.metrics_tracker.log_satisfaction(score)
            st.success(f"Thank you for your {score}-star rating!")

elif page == "📊 Dashboard":
    st.markdown('<h1 class="main-header">Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load customer data
    try:
        customer_df = DataProcessor.load_customer_data('data/customer_data.csv')
        
        if not customer_df.empty:
            # Overview metrics
            st.subheader("📈 Customer Overview")
            metrics = DataProcessor.calculate_customer_metrics(customer_df)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Customers", metrics['total_customers'])
            col2.metric("Avg Monthly Spend", f"₦{metrics['avg_monthly_spend']:.0f}")
            col3.metric("Avg Tenure", f"{metrics['avg_tenure']:.1f} months")
            col4.metric("Total Complaints", int(metrics['total_complaints']))
            
            # Churn Analysis
            st.markdown("---")
            st.subheader("🎯 Churn Prediction Analysis")
            
            if st.button("🔮 Run Churn Prediction"):
                with st.spinner("Analyzing churn risk..."):
                    predictions = st.session_state.churn_predictor.predict(customer_df)
                    st.session_state.predictions = predictions
                st.success("Churn prediction completed!")
            
            if 'predictions' in st.session_state:
                pred_df = st.session_state.predictions
                
                col1, col2, col3 = st.columns(3)
                col1.metric("High Risk Customers", 
                           len(pred_df[pred_df['risk_level'] == 'High']))
                col2.metric("Medium Risk Customers",
                           len(pred_df[pred_df['risk_level'] == 'Medium']))
                col3.metric("Low Risk Customers",
                           len(pred_df[pred_df['risk_level'] == 'Low']))
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    # Risk distribution
                    risk_counts = pred_df['risk_level'].value_counts()
                    fig = px.pie(values=risk_counts.values, names=risk_counts.index,
                                title="Churn Risk Distribution",
                                color_discrete_sequence=['#28a745', '#ffc107', '#dc3545'])
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Churn probability distribution
                    fig = px.histogram(pred_df, x='churn_probability',
                                      title="Churn Probability Distribution",
                                      nbins=20, color_discrete_sequence=['#FFCC00'])
                    st.plotly_chart(fig, use_container_width=True)
                
                # High risk customers table
                st.subheader("⚠️ High Risk Customers")
                high_risk = pred_df[pred_df['risk_level'] == 'High'].sort_values(
                    'churn_probability', ascending=False
                )
                st.dataframe(high_risk[['customer_id', 'tenure_months', 'monthly_spend', 
                                       'complaints', 'churn_probability', 'risk_level']], 
                            use_container_width=True)
            
            # Conversation Analytics
            st.markdown("---")
            st.subheader("💬 Conversation Analytics")
            
            conv_metrics = st.session_state.metrics_tracker.get_summary()
            
            if conv_metrics['total_conversations'] > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Intent distribution
                    intent_dist = conv_metrics['intent_distribution']
                    if intent_dist:
                        fig = px.bar(x=list(intent_dist.keys()), y=list(intent_dist.values()),
                                    title="Intent Distribution",
                                    labels={'x': 'Intent', 'y': 'Count'},
                                    color_discrete_sequence=['#FFCC00'])
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Metrics over time
                    st.metric("Average Confidence", f"{conv_metrics['avg_confidence']:.2%}")
                    st.metric("Average Response Time", f"{conv_metrics['avg_response_time']:.2f}s")
                    if conv_metrics['avg_satisfaction'] > 0:
                        st.metric("Customer Satisfaction", f"{conv_metrics['avg_satisfaction']:.1f}/5")
            else:
                st.info("No conversation data available yet. Start chatting to see analytics!")
        
        else:
            st.warning("No customer data available. Please upload data in the Admin Panel.")
    
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

elif page == "🔧 Admin Panel":
    st.markdown('<h1 class="main-header">Admin Panel</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 FAQ Management", "🤖 Model Training", "📥 Data Upload"])
    
    with tab1:
        st.subheader("FAQ Management")
        
        # Scrape FAQs
        if st.button("🌐 Scrape MTN Website FAQs"):
            with st.spinner("Scraping FAQs from mtn.ng..."):
                scraper = FAQScraper()
                faqs = scraper.scrape_social_bundles_faq()
                scraper.save_to_file(faqs)
            st.success(f"Successfully scraped {len(faqs)} FAQs!")
            st.rerun()
        
        # Display current FAQs
        st.markdown("---")
        st.subheader("Current FAQ Database")
        
        all_faqs = st.session_state.chat_engine.all_faqs
        if all_faqs:
            st.write(f"Total FAQs: {len(all_faqs)}")
            
            # Show FAQs in expandable sections
            for i, faq in enumerate(all_faqs[:10]):  # Show first 10
                with st.expander(f"❓ {faq['question']}"):
                    st.write(f"**Answer:** {faq['answer']}")
                    st.write(f"**Category:** {faq.get('category', 'N/A')}")
                    if 'source' in faq:
                        st.write(f"**Source:** {faq['source']}")
            
            if len(all_faqs) > 10:
                st.info(f"Showing 10 of {len(all_faqs)} FAQs")
        else:
            st.warning("No FAQs loaded")
    
    with tab2:
        st.subheader("Churn Prediction Model Training")
        
        st.info("Train the churn prediction model using customer data")
        
        if st.button("🎓 Train Model"):
            with st.spinner("Training churn prediction model..."):
                try:
                    metrics = st.session_state.churn_predictor.train()
                    
                    st.success("Model training completed!")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("AUC Score", f"{metrics['auc']:.4f}")
                    col2.metric("Target", "> 0.7")
                    
                    if metrics['auc'] > 0.7:
                        st.success("✅ Model meets performance target!")
                    else:
                        st.warning("⚠️ Model below performance target")
                    
                    # Feature importance
                    st.subheader("Feature Importance")
                    importance = metrics['feature_importance']
                    fig = px.bar(x=list(importance.values()), y=list(importance.keys()),
                                orientation='h', title="Feature Importance",
                                labels={'x': 'Importance', 'y': 'Feature'},
                                color_discrete_sequence=['#FFCC00'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Classification report
                    with st.expander("📊 Detailed Classification Report"):
                        st.text(metrics['classification_report'])
                
                except Exception as e:
                    st.error(f"Error training model: {str(e)}")
    
    with tab3:
        st.subheader("Data Upload")
        
        # Upload customer data
        st.markdown("#### Upload Customer Data (CSV)")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Preview:")
                st.dataframe(df.head())
                
                # Validate
                validation = DataProcessor.validate_customer_data(df)
                
                if validation['valid']:
                    st.success("✅ Data validation passed!")
                    
                    if st.button("💾 Save Data"):
                        df.to_csv('data/customer_data.csv', index=False)
                        st.success("Data saved successfully!")
                else:
                    st.error(f"❌ Validation failed: {validation['error']}")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

elif page == "ℹ️ About":
    st.markdown('<h1 class="main-header">About MTN SmartAssist</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎯 Project Overview
    
    MTN SmartAssist is an AI-powered customer service assistant designed for MTN Nigeria's 
    Product Management for AI & Data Analytics training program. Use with caution.
    
    ### ✨ Key Features
    
    1. **Conversational AI Interface**
       - Natural language understanding
       - Intent classification
       - Context-aware responses
       - MTN brand-consistent tone
    
    2. **Churn Prediction Module**
       - Gradient Boosting classifier
       - Risk scoring (Low/Medium/High)
       - Feature importance analysis
       - AUC > 0.7 performance target
    
    3. **Conversation Summarization**
       - Automatic chat log summarization
       - CRM-ready notes generation
       - Key points extraction
    
    4. **Analytics Dashboard**
       - Real-time conversation metrics
       - Customer segmentation
       - Churn risk visualization
       - Performance tracking
    
    ### 🛠️ Technology Stack
    
    - **Frontend:** Streamlit
    - **AI/ML:** OpenAI GPT / Anthropic Claude
    - **ML Models:** Scikit-learn (Gradient Boosting)
    - **Data Processing:** Pandas, NumPy
    - **Visualization:** Plotly
    - **Web Scraping:** BeautifulSoup, Requests
    
    ### 📊 Evaluation Metrics
    
    - **Response Relevance:** User feedback and ratings
    - **Churn Prediction:** AUC > 0.7
    - **Response Latency:** < 3 seconds target
    - **Customer Satisfaction:** 5-star rating system
    
    ### 🚀 Getting Started
    
    1. Configure API keys in `.env` file
    2. Install dependencies: `pip install -r requirements.txt`
    3. Run the app: `streamlit run app.py`
    4. Start chatting with MTN SmartAssist!
    
    ### 📝 Demo Use Cases
    
    - "What data plans are available?"
    - "How do I check my balance?"
    - "I'm having network issues"
    - "How do I recharge my line?"
    - "Tell me about social bundles"
    
    ### 👥 Training Program
    
    This MVP demonstrates practical applications of AI in telecom customer service,
    including NLP, machine learning, and data analytics for business insights.
    
    ---
    
    **Built for MTN Nigeria Product Management Training**
    
    *Version 1.0 - Demo MVP*
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "MTN SmartAssist © 2025 | Built for MTN Nigeria Training Program"
    "</div>",
    unsafe_allow_html=True
)
