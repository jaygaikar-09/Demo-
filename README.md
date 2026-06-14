# 🧠 MindFlex AI - Emotion-Aware Virtual Learning Assistant

MindFlex AI is an interactive, premium AI-powered tutor designed to adapt to a student's emotional and cognitive state in real-time. Built for hackathons, it showcases a fully functional glassmorphic UI, dynamic learning modules, native browser text-to-speech, and a smart dual-LLM system (Local Ollama / Groq Cloud).

---

## 🌟 Key Features

1. **🎭 Real-Time Emotion-Adaptive Tutoring**
   - **Focused 🟢**: Concise, professional step-by-step notes with mathematical formulas and common edge cases.
   - **Confused 🟠**: Highly supportive, encouraging tone starting with checkpoints, using real-world analogies (e.g. food recipes, box packing) rather than dense jargon.
   - **Engaged 🟣**: Active challenges presenting concrete practice problems directly in the chat interface.

2. **🤖 Heuristic Auto-Emotion Detection**
   - The tutor automatically scans the student's inputs for sentiment indicators. If the user types *"I'm stuck"* or *"practice problem"*, the tutor automatically switches state and adapts its teaching strategy.

3. **🔊 Native Browser Text-to-Speech (TTS)**
   - Click the **🔊** icon next to any tutor response to read the explanation aloud using browser-native SpeechSynthesis. No external subscription keys or servers required.

4. **⚡ Dual-LLM Backend (Hybrid Local / Cloud)**
   - **Local Ollama**: 100% offline, private inference using `qwen2.5:3b`.
   - **Groq Cloud API**: Blazing fast cloud generation using `llama-3.3-70b-versatile` (~1,000 tokens/sec).
   - Easily swap providers inside the app sidebar at runtime.

5. **📚 Interactive Lesson Modules & Concept Playgrounds**
   - Collapsible walkthrough steps powered by custom-drawn responsive CSS chevrons (supports offline/font-restricted environments cleanly).
   - Interactive calculators: Variable substitution visualizer, algebra discriminant solver, and physics kinetic energy net work calculator.

---

## 🛠️ Local Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/jaygaikar-09/mindflex-ai.git
cd mindflex-ai
```

### 2. Set up virtual environment
```bash
# Create environment
python -m venv .venv

# Activate environment (Windows)
.\.venv\Scripts\activate

# Activate environment (Mac/Linux)
source .venv/bin/activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Set up LLMs

* **For Local Ollama (Offline)**:
  1. Download and start [Ollama](https://ollama.com/).
  2. Pull the model in your terminal:
     ```bash
     ollama run qwen2.5:3b
     ```
  
* **For Groq Cloud (Ultra-fast)**:
  1. Generate an API Key at [console.groq.com](https://console.groq.com/).
  2. Add it to a `.env` file in the root of this project:
     ```env
     GROQ_API_KEY=gsk_your_key_here
     ```

### 5. Run the application
```bash
streamlit run index.py
```

---

## 🚀 Cloud Deployment (Streamlit Community Cloud)

Deploying a live shareable demo link takes less than 2 minutes:

1. Sign up/Log in at [share.streamlit.io](https://share.streamlit.io/) using your GitHub account.
2. Click **"New App"** and select this repository (`jaygaikar-09/mindflex-ai`).
3. Set the main file path to `index.py`.
4. Click **"Advanced settings..."** (next to the deploy button).
5. In the **Secrets** editor, paste your Groq API Key so it works automatically:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
6. Click **Save** and click **Deploy!**
