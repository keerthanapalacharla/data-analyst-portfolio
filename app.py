import os
import io
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import cv2
from PIL import Image, ImageDraw
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Safe MediaPipe Import Handling
# ---------------------------------------------------------
HAS_MEDIAPIPE = False
mp_pose = None
mp_drawing = None
mp_drawing_styles = None

try:
    import mediapipe as mp
    if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'pose'):
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        HAS_MEDIAPIPE = True
    else:
        import mediapipe.python.solutions.pose as mp_pose
        import mediapipe.python.solutions.drawing_utils as mp_drawing
        import mediapipe.python.solutions.drawing_styles as mp_drawing_styles
        HAS_MEDIAPIPE = True
except Exception:
    HAS_MEDIAPIPE = False

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="MorphoMama AI — Multimodal Postpartum Rehab",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fef2f2 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .header-container {
        background: linear-gradient(135deg, #ff9ca2 0%, #7c3aed 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.2);
    }
    .header-container h1 {
        color: white !important;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .header-container p {
        color: #fce7f3;
        font-size: 1.2rem;
        margin: 0;
    }
    .content-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 1.8rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-weight: 700;
        font-size: 1.25rem;
        color: #1e293b;
        margin-bottom: 0.8rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff9ca2 0%, #7c3aed 100%);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 700;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.3);
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Secure API Key Setup
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

client = None
if api_key:
    client = genai.Client(
        api_key=api_key.strip(),
        http_options=types.HttpOptions(api_version="v1beta")
    )

def safe_generate_content(client, model, contents, max_retries=3):
    """
    Executes generate_content with exponential backoff to recover from 503 server demand spikes.
    """
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents
            )
        except Exception as e:
            err_msg = str(e)
            if ("503" in err_msg or "UNAVAILABLE" in err_msg or "high demand" in err_msg) and attempt < max_retries - 1:
                time.sleep((2 ** attempt) + 1)  # Delays: 2s, 3s, 5s
                continue
            raise e

# Sidebar Setup
with st.sidebar:
    st.image("https://api.iconify.design/noto:pregnant-woman-light-skin-tone.svg", width=70)
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
    
    if HAS_MEDIAPIPE:
        st.success("🟢 MediaPipe Ready")
    else:
        st.warning("⚠️ MediaPipe Fallback Mode")
        
    st.caption("Powered by Gemini 1.5 Flash")

# Hero Banner
st.markdown("""
<div class="header-container">
    <h1>🧘‍♀️ MorphoMama AI</h1>
    <p>Empathetic Multimodal Support for Your Postpartum Wellness Journey</p>
</div>
""", unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3 = st.tabs([
    "🧠 Mental Health CBT Agent", 
    "🏋️ Physical Recovery & Posture", 
    "📊 Progress Analytics"
])

# ---------------------------------------------------------
# Tab 1: CBT Agent
# ---------------------------------------------------------
with tab1:
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.markdown("""
        <div class="content-card" style="text-align: center;">
            <span style="font-size: 5rem;">🤱</span>
            <h3 style="color: #475569; margin-top: 10px;">Safe Space for Moms</h3>
            <p style="color: #64748b; font-size: 0.95rem;">
                Prioritize your emotional well-being with personalized cognitive behavioral reframing.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">🧠 Sentiment Screening</div>
            <p style="color: #64748b;">Share your thoughts below to receive warm, validated CBT reframing and grounding exercises.</p>
        </div>
        """, unsafe_allow_html=True)
        
        user_input = st.text_area(
            "My reflections today...", 
            placeholder="I feel overwhelmed by mood shifts and daily tasks...",
            height=130
        )
        
        if st.button("RUN CBT SENTIMENT ANALYSIS"):
            if not client:
                st.error("API Key not initialized. Please set GEMINI_API_KEY environment variable.")
            elif not user_input.strip():
                st.warning("Please enter your thoughts before running the analysis.")
            else:
                with st.spinner("Analyzing with Gemini..."):
                    try:
                        prompt = f"""
                        Act as an empathetic maternal mental health professional. 
                        Analyze the user reflection and provide:
                        1. A warm, validated response.
                        2. 2 simple grounding cognitive behavioral exercise techniques.
                        
                        User reflection: "{user_input}"
                        """
                        response = safe_generate_content(
                            client=client,
                            model="gemini-1.5-flash", 
                            contents=prompt
                        )
                        st.markdown(f"""
                        <div class="content-card">
                            <div class="card-title">💡 Recommended CBT Insights</div>
                            <p style="color: #334155; line-height: 1.6;">{response.text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        if "503" in str(e) or "UNAVAILABLE" in str(e):
                            st.warning("🌸 The AI service is experiencing high demand right now. Please wait a moment and click 'RUN CBT SENTIMENT ANALYSIS' again.")
                        else:
                            st.error(f"Error calling Gemini API: {str(e)}")

# ---------------------------------------------------------
# Tab 2: Physical Recovery & Posture (STABLE CAMERA CAPTURE)
# ---------------------------------------------------------
with tab2:
    st.markdown("""
    <div class="content-card">
        <div class="card-title">🏋️ Pose Rehab Coach & Posture Analysis</div>
        <p style="color: #64748b;">Follow the countdown guide, step back into posture position, and take or upload your exercise photo/video.</p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Spine Alignment Score", "84%", "+5% vs Week 2")
    m2.metric("Diastasis Recti Gap", "1.8 cm", "-0.3 cm vs Week 2")
    m3.metric("Pelvic Floor Strength", "6/10", "+1 vs Baseline")
    
    st.write("")
    
    col_select, col_capture = st.columns([1, 2], gap="large")
    
    with col_select:
        st.markdown("**1. Select Exercise & Read Guide**")
        selected_ex = st.selectbox("Current Exercise:", ["Pelvic Tilt", "Glute Bridge", "Diaphragmatic Breathing"], index=0)
        
        exercise_details = {
            "Pelvic Tilt": ("🧘‍♀️", "Target: Spine Alignment. Lie on side/back, align full torso in camera frame."),
            "Glute Bridge": ("🏋️‍♀️", "Target: Core/Hips. Elevate hips toward ceiling, keep knees aligned."),
            "Diaphragmatic Breathing": ("𝄠", "Target: Core. Deep abdominal expansion and controlled exhalation.")
        }
        
        icon, desc = exercise_details[selected_ex]
        st.markdown(f"""
        <div class="content-card" style="text-align: center; background-color: #faf5ff;">
            <span style="font-size: 3.5rem;">{icon}</span>
            <h4 style="color: #7c3aed; margin-top: 10px;">{selected_ex} Guidelines</h4>
            <p style="color: #475569; font-size: 0.95rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_capture:
        st.markdown("**2. Posture Capture**")
        
        input_mode = st.radio("Choose Input Type:", ["📸 Standard Camera Capture", "🎥 Upload Exercise Video"], horizontal=True)
        
        if input_mode == "📸 Standard Camera Capture":
            # 5-Second Timer Assistant
            if st.button("⏱️ START 5-SECOND TIMER ASSISTANT"):
                countdown_placeholder = st.empty()
                for i in range(5, 0, -1):
                    countdown_placeholder.markdown(f"""
                    <div style="font-size: 4rem; color: #7c3aed; font-weight: 800; text-align: center;">
                        Get in Position: {i}s
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                countdown_placeholder.success("📸 FREEZE POSTURE & TAKE PHOTO NOW!")
            
            camera_image = st.camera_input("Capture Posture Snapshot")
            
            if camera_image:
                file_bytes = np.frombuffer(camera_image.getvalue(), dtype=np.uint8)
                image_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
                
                detected = False
                if HAS_MEDIAPIPE and mp_pose:
                    try:
                        with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
                            results = pose.process(image_rgb)
                            if results.pose_landmarks:
                                mp_drawing.draw_landmarks(
                                    image_rgb,
                                    results.pose_landmarks,
                                    mp_pose.POSE_CONNECTIONS,
                                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                                )
                                detected = True
                                st.success("✅ Skeleton joints overlayed via MediaPipe!")
                    except Exception:
                        detected = False
                
                if not detected:
                    st.info("ℹ️ Proceeding with Direct Gemini Vision Posture Analysis.")
                
                st.image(image_rgb, caption="Posture Alignment Snapshot", use_container_width=True)
                
                if client:
                    with st.spinner(f"Evaluating posture form for {selected_ex}..."):
                        try:
                            bytes_data = camera_image.getvalue()
                            image_part = types.Part.from_bytes(data=bytes_data, mime_type="image/jpeg")
                            
                            prompt = f"""
                            Act as a physical therapy posture specialist evaluating a postpartum recovery exercise: '{selected_ex}'.
                            Analyze this snapshot and provide structured feedback:
                            1. **Form Status**: State clearly 'CORRECT' or 'NEEDS ADJUSTMENT'
                            2. **Posture Score**: Give a percentage score (e.g. 85%)
                            3. **Spine & Joint Alignment**: Describe neck, shoulder, and lumbar alignment observed.
                            4. **Correction Steps**: Give 2 actionable posture adjustments to improve execution.
                            """
                            
                            eval_response = safe_generate_content(
                                client=client,
                                model="gemini-1.5-flash",
                                contents=[image_part, prompt]
                            )
                            
                            st.markdown(f"""
                            <div class="content-card">
                                <div class="card-title">🎯 Posture Evaluation Verdict</div>
                                <p style="color: #334155; line-height: 1.6;">{eval_response.text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.warning(f"Gemini API response note: {str(e)}")
                            
        elif input_mode == "🎥 Upload Exercise Video":
            uploaded_video = st.file_uploader(f"Upload recorded video of {selected_ex}:", type=["mp4", "mov", "avi"])
            if uploaded_video:
                st.video(uploaded_video)
                if st.button(f"ANALYZE {selected_ex.upper()} VIDEO"):
                    if client:
                        with st.spinner("Analyzing motion with Gemini..."):
                            try:
                                video_bytes = uploaded_video.getvalue()
                                mime_type = uploaded_video.type or "video/mp4"
                                video_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
                                
                                prompt = f"""
                                Act as a physical therapist specializing in postpartum recovery. 
                                Evaluate this video of a patient doing: '{selected_ex}'.
                                Provide:
                                1. **Pacing & Breathing Assessment**: (Analyze rhythm and abdominal movement)
                                2. **Form Accuracy**: (State CORRECT or NEEDS ADJUSTMENT with percentage score)
                                3. **2 Specific Safety & Performance Feedback Points**
                                """
                                
                                video_analysis = safe_generate_content(
                                    client=client,
                                    model="gemini-1.5-flash",
                                    contents=[video_part, prompt]
                                )
                                
                                st.markdown(f"""
                                <div class="content-card">
                                    <div class="card-title">📹 Video Movement Analysis</div>
                                    <p style="color: #334155; line-height: 1.6;">{video_analysis.text}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Video analysis error: {str(e)}")

# ---------------------------------------------------------
# Tab 3: Progress Analytics
# ---------------------------------------------------------
with tab3:
    st.markdown("""
    <div class="content-card">
        <div class="card-title">📊 14-Day Recovery Trend</div>
        <p style="color: #64748b;">Aggregated recovery metrics across physical posture scores and emotional well-being screening.</p>
    </div>
    """, unsafe_allow_html=True)
    
    days = [f"Day {i}" for i in range(1, 15)]
    np.random.seed(42)
    cbt_scores = np.random.randint(4, 10, size=14)
    posture_scores = np.random.randint(60, 95, size=14)
    
    df = pd.DataFrame({
        "Day": days,
        "Mental Well-being (1-10)": cbt_scores,
        "Posture Score (%)": posture_scores
    })
    
    fig = px.line(
        df, 
        x="Day", 
        y=["Mental Well-being (1-10)", "Posture Score (%)"],
        markers=True,
        color_discrete_sequence=["#ff9ca2", "#7c3aed"]
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)