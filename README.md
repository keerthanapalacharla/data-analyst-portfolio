# 🧘‍♀️ MorphoMama AI – Multimodal Postpartum Rehab Suite

> **An all-in-one postpartum recovery platform powered by Google Gemini 3.6 Flash.**

MorphoMama AI bridges critical gaps in maternal healthcare by combining empathetic Cognitive Behavioral Therapy (CBT) support with real-time posture tracking for safe physical recovery and comprehensive clinical analytics.

---

## 🌟 Key Features

* **🧠 EPDS CBT Agent:** Validates maternal emotional distress, provides personalized cognitive reframing, and recommends tailored grounding or breathing techniques powered by `gemini-3.6-flash`.
* **🏋️ Posture Coach:** Provides real-time exercise feedback for core and pelvic floor rehabilitation (e.g., pelvic tilts, bridges) to prevent diastasis recti, supporting live webcam snapshots and pose assessments.
* **📊 BigQuery Clinical Analytics:** Tracks population-level recovery risk benchmarks, recovery metrics, and 14-day progress trends across postpartum weeks.

---

## 🛠️ Tech Stack

* **AI Model:** Google Gemini API (`gemini-3.6-flash` via `google-genai` SDK)
* **Frontend UI:** Streamlit
* **Hosting & Cloud:** Google Cloud Run (Containerized via Docker)
* **Data & Analytics:** Python, Pandas, NumPy, Plotly Express

---

## 🔒 Security & Secret Management

* **Zero Hardcoded Secrets:** No API keys, passwords, or credentials are stored inside the code repository.
* **Runtime Secret Injection:** `GEMINI_API_KEY` is securely injected into the container environment via Google Cloud Run configuration flags.
* **SDK Isolation:** Enforces `GOOGLE_GENAI_USE_VERTEXAI=false` to isolate developer API keys from default environment credentials.

---

## 🚀 Quickstart, Setup & Deployment

### 1. Local Setup

Clone the repository and install the dependencies:

```bash
git clone [https://github.com/keerthanapalacharla/data-analyst-portfolio.git](https://github.com/keerthanapalacharla/data-analyst-portfolio.git)
cd data-analyst-portfolio
pip install -r requirements.txt

$env:GEMINI_API_KEY="your_api_key_here"
streamlit run app.py

export GEMINI_API_KEY="your_api_key_here"
streamlit run app.py

gcloud run deploy morphomama-ai \
  --source . \
  --region us-central1 \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=false,GEMINI_API_KEY=your_api_key_here"
