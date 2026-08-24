import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="MorphoMama AI — Multimodal Postpartum Rehab",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern CSS Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .header-container {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
    }
    .header-container h1 {
        color: white !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .header-container p {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin: 0;
    }
    .content-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Secure API Key Setup & Client Initialization
# Strictly reads from Environment Variables
# ---------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

client = None
if api_key:
    client = genai.Client(
        api_key=api_key.strip(),
        http_options=types.HttpOptions(api_version="v1beta")
    )

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    # Fixed sidebar image using reliable Iconify CDN asset
    st.image("https://api.iconify.design/emojione-v1:pregnant-woman.svg", width=64)
    st.title("MorphoMama AI")
    st.caption("Postpartum Multimodal Recovery Suite")
    st.divider()
    
    st.markdown("### 🚨 Emergency Support")
    st.info("""
    **Maternal Mental Health:**  
    📞 **1-833-852-6262**
    
    **Suicide & Crisis Lifeline:**  
    📞 **988 (US)**
    """)
    st.divider()
    
    if client:
        st.success("🟢 Gemini API Ready")
    else:
        st.error("⚠️ GEMINI_API_KEY Missing")

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <h1>🧘‍♀️ MorphoMama AI</h1>
    <p>Multimodal Postpartum Physical & Mental Rehabilitation Assistant</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Tabs
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🧠 CBT Mental Health Agent", 
    "🏋️ Posture Rehabilitation", 
    "📊 BigQuery Clinical Analytics"
])

# ---------------------------------------------------------
# Tab 1: CBT Mental Health Agent
# ---------------------------------------------------------
with tab1:
    st.subheader("Mindfulness & Sentiment Screening")
    st.write("Share how you are feeling today to receive empathetic, grounding CBT insights.")
    
    user_input = st.text_area(
        "How are you feeling right now?", 
        placeholder="I feel exhausted, overwhelmed by mood shifts, and unable to balance daily tasks...",
        height=120
    )
    
    if st.button("Run CBT Sentiment Analysis"):
        if not client:
            st.error("API Key not initialized correctly.")
        elif not user_input.strip():
            st.warning("Please enter your thoughts before running the analysis.")
        else:
            with st.spinner("Analyzing response with Gemini..."):
                try:
                    prompt = f"""
                    Act as an empathetic maternal mental health professional. 
                    Analyze the following user reflection and provide:
                    1. A warm, validated response.
                    2. 2 simple grounding cognitive behavioral exercise techniques.
                    
                    User reflection: "{user_input}"
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-3.6-flash", 
                        contents=prompt
                    )
                    
                    st.markdown("### 💡 Recommended CBT Insights")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error calling Gemini API: {str(e)}")

# ---------------------------------------------------------
# Tab 2: Posture Rehabilitation
# ---------------------------------------------------------
with tab2:
    st.subheader("Real-Time Physical Recovery Assistant")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Live Posture Tracker**")
        camera_image = st.camera_input("Capture pose assessment")
    with col2:
        st.markdown("**Posture Metrics**")
        m1, m2 = st.columns(2)
        m1.metric("Spine Alignment Score", "84%", "+5%")
        m2.metric("Diastasis Recti Gap", "1.8 cm", "-0.3 cm")
        
        st.markdown("""
        <div class="content-card">
            <h4>📋 Today's Recommended Protocol</h4>
            <ul>
                <li><strong>Pelvic Tilt Hold:</strong> 3 sets x 10 reps</li>
                <li><strong>Diaphragmatic Breathing:</strong> 5 minutes</li>
                <li><strong>Cat-Cow Spine Stretch:</strong> 2 sets x 8 reps</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 3: Clinical Analytics
# ---------------------------------------------------------
with tab3:
    st.subheader("Patient Progress Dashboard")
    days = [f"Day {i}" for i in range(1, 15)]
    np.random.seed(42)
    cbt_scores = np.random.randint(4, 10, size=14)
    posture_scores = np.random.randint(60, 95, size=14)
    
    df = pd.DataFrame({
        "Day": days,
        "Mental Well-being (1-10)": cbt_scores,
        "Posture Score (%)": posture_scores
    })
    
    st.markdown("**14-Day Recovery Trend**")
    fig = px.line(
        df, 
        x="Day", 
        y=["Mental Well-being (1-10)", "Posture Score (%)"],
        markers=True,
        color_discrete_sequence=["#4f46e5", "#10b981"]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)