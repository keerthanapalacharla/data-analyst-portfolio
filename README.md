# 🧘‍♀️ MorphoMama AI — Multimodal Postpartum Recovery Suite

MorphoMama AI is an empathetic, AI-powered recovery application designed to support postpartum mothers through cognitive behavioral therapy (CBT) reframing, real-time computer vision posture analysis, and progress tracking.

🌐 **Live Demo:** [MorphoMama AI on Google Cloud Run](https://morphomama-ai-311802279482.us-central1.run.app)

## ✨ Key Features
- **🧠 Mental Health CBT Agent:** Empathetic text analysis using Gemini 1.5 Flash to provide emotional validation and structured grounding exercises.
- **🏋️ Physical Recovery & Posture Coach:** Real-time pose landmark extraction via MediaPipe combined with Gemini Vision for posture alignment feedback and exercise video evaluation.
- **📊 Progress Analytics:** Interactive 14-day recovery trend visualizations comparing emotional well-being and posture scores using Plotly.

## 🛠️ Tech Stack
- **Frontend & App Framework:** Streamlit, Custom CSS
- **AI & Vision Models:** Google Gemini API (`google-genai` SDK), MediaPipe Pose, OpenCV
- **Data Analytics:** Plotly Express, Pandas, NumPy
- **Deployment & Cloud:** Google Cloud Run, Docker
