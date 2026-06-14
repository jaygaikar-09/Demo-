import streamlit as st
import requests
from dotenv import load_dotenv
import textwrap

load_dotenv()

import json

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        default_users = {"student": "mindflex", "admin": "admin"}
        try:
            with open(USERS_FILE, "w") as f:
                json.dump(default_users, f)
        except Exception:
            pass
        return default_users

def save_user(username, password):
    users = load_users()
    users[username.lower()] = password
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)
        return True
    except Exception:
        return False


st.set_page_config(
    page_title="MindFlex AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/chat"

LESSONS = {
    "📐 Calculus - Integration by Substitution": {
        "notes": """Topic: Calculus - Integration by Substitution
Goal: Simplify integrals of composite functions.
Step 1: Choose a substitution u = g(x)
Step 2: Find du = g'(x)dx
Step 3: Substitute into the integral
Step 4: Integrate with respect to u
Step 5: Replace u with g(x)

Example:
∫ 2x cos(x²) dx
Let: u = x², du = 2x dx
Integral becomes: ∫ cos(u) du""",
        "steps": [
            {"title": "Step 1: Choose substitution u = g(x)", "content": "Look for a function inside another function. For $\\int 2x \\cos(x^2) dx$, let $u = x^2$."},
            {"title": "Step 2: Find du = g'(x)dx", "content": "Differentiate $u$. Since $u = x^2$, the derivative is $2x$, so $du = 2x dx$."},
            {"title": "Step 3: Substitute into the integral", "content": "Replace $x^2$ with $u$ and $2x dx$ with $du$. The integral becomes $\\int \\cos(u) du$."},
            {"title": "Step 4: Integrate with respect to u", "content": "Integrate $\\cos(u)$ to get $\\sin(u) + C$."},
            {"title": "Step 5: Replace u with original g(x)", "content": "Substitute back $u = x^2$. The final answer is $\\sin(x^2) + C$."}
        ]
    },
    "📊 Algebra - Quadratic Formula": {
        "notes": """Topic: Algebra - Quadratic Formula
Goal: Solve quadratic equations of the form ax² + bx + c = 0.
Step 1: Identify coefficients a, b, c
Step 2: Calculate the discriminant D = b² - 4ac
Step 3: Apply the quadratic formula x = (-b ± √D) / 2a

Example:
x² - 5x + 6 = 0
Let: a=1, b=-5, c=6
D = (-5)² - 4(1)(6) = 1""",
        "steps": [
            {"title": "Step 1: Identify coefficients", "content": "For $x^2 - 5x + 6 = 0$, coefficients are $a=1$, $b=-5$, $c=6$."},
            {"title": "Step 2: Calculate Discriminant D = b² - 4ac", "content": "Compute $D = (-5)^2 - 4(1)(6) = 25 - 24 = 1$. Since $D > 0$, there are two real roots."},
            {"title": "Step 3: Apply Quadratic Formula", "content": "Solve $x = \\frac{-(-5) \\pm \\sqrt{1}}{2(1)} = \\frac{5 \\pm 1}{2}$. Roots are $x=3$ and $x=2$."}
        ]
    },
    "🍎 Physics - Work-Energy Theorem": {
        "notes": """Topic: Physics - Work-Energy Theorem
Goal: Relate the work done on an object to its change in kinetic energy.
Formula: W_net = ΔK = 1/2 m v_f² - 1/2 m v_i²
Step 1: Identify mass (m) and velocities (v_i, v_f)
Step 2: Calculate Net Work done

Example:
An object of mass 2kg accelerates from 2m/s to 4m/s.
ΔK = 1/2 * 2 * (16 - 4) = 12 Joules.
Net Work = 12 Joules.""",
        "steps": [
            {"title": "Step 1: Identify parameters", "content": "Find the mass of the object $m$, initial velocity $v_i$, and final velocity $v_f$."},
            {"title": "Step 2: Relate Net Work to Kinetic Energy", "content": "Net Work $W_{net}$ equals the change in kinetic energy $\\Delta K = K_f - K_i = \\frac{1}{2}mv_f^2 - \\frac{1}{2}mv_i^2$."}
        ]
    }
}


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

/* Main font styling */
html, body, p, li, a, strong, em, button, select, input, textarea, h1, h2, h3, h4, h5, h6, .stMarkdown {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Base page background styling */
[data-testid="stAppViewContainer"] {
    background-color: #030712;
    background-image: radial-gradient(at 0% 0%, rgba(17, 24, 39, 0.8) 0, transparent 50%), radial-gradient(at 50% 0%, rgba(31, 41, 55, 0.3) 0, transparent 50%);
    color: #f3f4f6;
}

[data-testid="stSidebar"] {
    background-color: #0b0f19;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Glassmorphism panels */
div[data-testid="stColumn"] {
    background: rgba(17, 24, 39, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s ease;
}

/* Accent borders on columns */
div[data-testid="stColumn"]:hover {
    border-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

/* Reset nested columns inside chat messages and other column groupings */
div[data-testid="stChatMessage"] div[data-testid="stColumn"],
div[data-testid="stColumn"] div[data-testid="stColumn"] {
    background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    transform: none !important;
}

/* Chat container glassmorphism */
div[data-testid="stElementContainer"] > div[style*="height"] {
    background: rgba(15, 23, 42, 0.4) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 12px;
}

/* Avatar Card */
.avatar-card {
    text-align: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.avatar-emoji {
    font-size: 64px;
    margin-bottom: 12px;
    animation: pulse 2s infinite ease-in-out;
}

.avatar-status {
    font-size: 13px;
    color: #9ca3af;
    line-height: 1.4;
    margin-top: 8px;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
}

.badge {
    font-size: 10px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 12px;
    display: inline-block;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Custom styled scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Custom offline CSS chevrons for Streamlit expander headers to prevent text overlap */
summary span > span > span {
    font-size: 0px !important;
    color: transparent !important;
    display: none !important;
}

summary span > span {
    width: 8px !important;
    height: 8px !important;
    border-right: 2px solid rgba(255, 255, 255, 0.7) !important;
    border-bottom: 2px solid rgba(255, 255, 255, 0.7) !important;
    transform: rotate(-45deg) !important; /* Pointing right */
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: inline-block !important;
    margin-right: 12px !important;
    margin-left: 4px !important;
    margin-top: -2px !important;
    vertical-align: middle !important;
}

details[open] summary span > span {
    transform: rotate(45deg) !important; /* Pointing down */
}
</style>
""", unsafe_allow_html=True)



if "emotion" not in st.session_state:
    st.session_state.emotion = "focused"

if "current_topic" not in st.session_state:
    st.session_state.current_topic = list(LESSONS.keys())[0]

if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "🤖 Local Ollama"

if "groq_api_key" not in st.session_state:
    import os
    # Try fetching from Streamlit secrets, then environment variables
    api_key = ""
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "")
    st.session_state.groq_api_key = api_key

# --- USER AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat_interactions" not in st.session_state:
    st.session_state.chat_interactions = 0

if "labs_explored" not in st.session_state:
    st.session_state.labs_explored = set()

if "tts_reads" not in st.session_state:
    st.session_state.tts_reads = 0

if "moods_experienced" not in st.session_state:
    st.session_state.moods_experienced = {"focused": 1, "confused": 0, "engaged": 0}

if not st.session_state.logged_in:
    st.markdown(textwrap.dedent("""
    <div style="text-align: center; margin-top: 40px; margin-bottom: 30px;">
        <h1 style="font-size: 44px; font-weight: 700; color: #f3f4f6; margin-bottom: 5px; letter-spacing: -0.5px;">🧠 MindFlex AI</h1>
        <p style="color: #9ca3af; font-size: 16px; font-weight: 400; margin-top: 0;">Emotion-Aware Virtual Learning Assistant</p>
    </div>
    """), unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(textwrap.dedent("""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.37);">
            <h2 style="color: #34d399; margin-top: 0; font-size: 24px; font-weight: 600; margin-bottom: 10px;">Core AI Capabilities</h2>
            <p style="color: #9ca3af; font-size: 13px; margin-bottom: 30px;">An adaptive tutoring space designed to meet your cognitive and emotional needs.</p>
            <div style="margin-bottom: 25px; display: flex; align-items: flex-start;">
                <div style="font-size: 24px; margin-right: 15px; margin-top: 2px;">🎭</div>
                <div>
                    <b style="color: #f3f4f6; font-size: 15px; display: block;">Emotion-Adaptive Explanations</b>
                    <span style="color: #9ca3af; font-size: 13px; display: block; margin-top: 2px;">Dynamically adapts tutoring style to patient recipes for confusion, precise layouts for focus, and challenges for interest.</span>
                </div>
            </div>
            <div style="margin-bottom: 25px; display: flex; align-items: flex-start;">
                <div style="font-size: 24px; margin-right: 15px; margin-top: 2px;">🤖</div>
                <div>
                    <b style="color: #f3f4f6; font-size: 15px; display: block;">Heuristic Sentiment Detection</b>
                    <span style="color: #9ca3af; font-size: 13px; display: block; margin-top: 2px;">Automatically identifies confusion or interest flags directly in student prompt inputs to swap states instantly.</span>
                </div>
            </div>
            <div style="margin-bottom: 25px; display: flex; align-items: flex-start;">
                <div style="font-size: 24px; margin-right: 15px; margin-top: 2px;">🔊</div>
                <div>
                    <b style="color: #f3f4f6; font-size: 15px; display: block;">Instant Speech Synthesis (TTS)</b>
                    <span style="color: #9ca3af; font-size: 13px; display: block; margin-top: 2px;">Converts text answers into audible speech right inside your browser window with zero API latency.</span>
                </div>
            </div>
            <div style="display: flex; align-items: flex-start;">
                <div style="font-size: 24px; margin-right: 15px; margin-top: 2px;">🛠️</div>
                <div>
                    <b style="color: #f3f4f6; font-size: 15px; display: block;">Concept Play Laboratories</b>
                    <span style="color: #9ca3af; font-size: 13px; display: block; margin-top: 2px;">Hands-on calculators and graphers to visualize variables swap steps and solve quadratic algebra metrics.</span>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
        <div style="background: rgba(17, 24, 39, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 25px 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); text-align: center; display: flex; flex-direction: column;">
            <div style="font-size: 36px; margin-bottom: 10px;">🧑‍🎓</div>
            <h3 style="margin-top: 0; margin-bottom: 5px; color: #f3f4f6; font-size: 20px; font-weight: 600;">Student Access Portal</h3>
            <p style="color: #6b7280; font-size: 12px; margin-bottom: 20px;">Access your personalized learning profile and AI tutor.</p>
        """), unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up"])
        
        users = load_users()
        
        with tab_login:
            login_user = st.text_input("Username", placeholder="e.g. student", key="login_username")
            login_pass = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            
            login_btn = st.button("Access Dashboard 🚀", use_container_width=True, key="login_btn_submit")
            
            if login_btn:
                login_user_clean = login_user.strip().lower()
                if not login_user_clean or not login_pass:
                    st.error("Fields cannot be empty!")
                elif login_user_clean in users and users[login_user_clean] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user_clean
                    st.toast(f"Welcome back, {login_user_clean.capitalize()}!", icon="🎉")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
                    
        with tab_signup:
            signup_user = st.text_input("Choose Username", placeholder="e.g. alex", key="signup_username")
            signup_pass = st.text_input("Choose Password", type="password", placeholder="••••••••", key="signup_password")
            signup_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")
            
            signup_btn = st.button("Create Account ✨", use_container_width=True, key="signup_btn_submit")
            
            if signup_btn:
                signup_user_clean = signup_user.strip().lower()
                if not signup_user_clean or not signup_pass:
                    st.error("Fields cannot be empty!")
                elif signup_pass != signup_confirm:
                    st.error("Passwords do not match!")
                elif signup_user_clean in users:
                    st.error("Username already exists!")
                else:
                    if save_user(signup_user_clean, signup_pass):
                        st.session_state.logged_in = True
                        st.session_state.username = signup_user_clean
                        st.toast(f"Account created! Welcome, {signup_user_clean.capitalize()}!", icon="✨")
                        st.rerun()
                    else:
                        st.error("Database save failed. Try again.")
                        
        st.markdown(textwrap.dedent("""
        <div style="margin-top: 30px; text-align: center; font-size: 11px; color: #4b5563; border-top: 1px solid rgba(255,255,255,0.03); padding-top: 10px;">
            🔑 <b>Default Access:</b> Username: <code style="color: #10b981;">student</code> | Password: <code style="color: #10b981;">mindflex</code>
        </div>
        </div>
        """), unsafe_allow_html=True)

    st.stop()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "text": "Hello! I am MindFlex AI. Ask me anything about today's lesson.",
            "badge": None
        }
    ]


THEMES = {
    "focused": {
        "name": "Focused 🟢",
        "color": "#34d399",
        "avatar": "🧐",
        "status": "Providing direct, structured, and precise step-by-step notes.",
        "glow": "rgba(52, 211, 153, 0.4)"
    },
    "confused": {
        "name": "Confused 🟠",
        "color": "#fbbf24",
        "avatar": "💡",
        "status": "Simplifying concepts, using real-world analogies, and breaking steps down.",
        "glow": "rgba(251, 191, 36, 0.4)"
    },
    "engaged": {
        "name": "Engaged 🟣",
        "color": "#a78bfa",
        "avatar": "🚀",
        "status": "Injecting active practice problems and tutoring challenges.",
        "glow": "rgba(167, 139, 250, 0.4)"
    }
}


def ask_ai(question, emotion, notes):
    provider = st.session_state.get("llm_provider", "🤖 Local Ollama")
    
    # 1. Build prompt based on student state (exactly matches main.py logic)
    emotion = emotion.lower()
    if emotion == "confused":
        system_instruction = (
            "You are an AI Tutor, a highly supportive, patient and encouraging teacher. "
            "The student is currently CONFUSED. Your absolute priority is to simplify. "
            "1. Start with supportive words (e.g., 'No worries, let's break this down together!').\n"
            "2. Use real-world analogies (e.g., comparing substitution to swapping labels or unpacking nested boxes).\n"
            "3. Avoid using overly dense mathematical terminology where simple words work.\n"
            "4. Keep explanations short, simple, and step-by-step. Avoid huge walls of text.\n"
            "5. End with a simple, encouraging question to check if they understand the first step.\n\n"
            f"Lesson Notes:\n{notes}"
        )
        user_prompt = (
            f"Student Question: {question}\n\n"
            "Explain step by step in extremely simple language with supportive analogies."
        )
    elif emotion == "engaged":
        system_instruction = (
            "You are an AI Tutor, an energetic, interactive and enthusiastic teacher. "
            "The student is highly ENGAGED and motivated. Your goal is to keep them challenged and active. "
            "1. Acknowledge their positive attitude briefly (e.g., 'Awesome! Let's put this into practice!').\n"
            "2. Provide a brief explanation of the requested concept, focusing on how to solve it.\n"
            "3. Present them with a concrete practice problem/exercise (similar to the example in the lesson notes) and ask them to try solving it.\n"
            "4. Keep the pacing dynamic and interactive.\n\n"
            f"Lesson Notes:\n{notes}"
        )
        user_prompt = (
            f"Student Question: {question}\n\n"
            "Explain briefly and present a practice problem for them to solve."
        )
    else:  # focused
        system_instruction = (
            "You are an AI Tutor, a precise and structured teacher. "
            "The student is FOCUSED and ready to learn. Your goal is to provide concise, structured explanations. "
            "1. Provide a direct, step-by-step explanation using clean formatting.\n"
            "2. Include the mathematical details and structured steps.\n"
            "3. Point out potential edge cases or tricky steps (e.g. constant of integration, finding du correctly).\n"
            "4. Keep explanations highly professional, concise, and structured.\n\n"
            f"Lesson Notes:\n{notes}"
        )
        user_prompt = (
            f"Student Question: {question}\n\n"
            "Explain step by step with clear math formatting and point out common edge cases."
        )

    # 2. Call the chosen LLM provider
    if provider == "⚡ Groq Cloud":
        api_key = st.session_state.get("groq_api_key", "").strip()
        if not api_key:
            try:
                if "GROQ_API_KEY" in st.secrets:
                    api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                pass
        if not api_key:
            import os
            api_key = os.environ.get("GROQ_API_KEY", "")
            
        if not api_key:
            return "⚠️ Please enter your Groq API Key in the sidebar to use Groq Cloud!"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                res_data = response.json()
                return res_data["choices"][0]["message"]["content"]
            else:
                error_msg = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get("error", {}).get("message", response.text)
                except Exception:
                    pass
                return f"❌ Groq API Error ({response.status_code}): {error_msg}"
        except Exception as e:
            return f"❌ Connection Error (Groq): {str(e)}"
            
    else:  # Local Ollama
        import ollama
        try:
            response = ollama.Client(host="http://127.0.0.1:11434").chat(
                model="qwen2.5:3b",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response["message"]["content"]
        except Exception as e:
            return (
                "❌ Connection Error (Ollama): Could not connect to local Ollama on http://localhost:11434.\n\n"
                "**To fix this:**\n"
                "1. Make sure the Ollama desktop application is running.\n"
                "2. Verify the model `qwen2.5:3b` is pulled by running: `ollama run qwen2.5:3b` in your terminal.\n"
                "3. Alternatively, switch to **⚡ Groq Cloud** in the sidebar!"
            )


def trigger_emotion(emotion):

    st.session_state.emotion = emotion

    if "moods_experienced" in st.session_state:
        st.session_state.moods_experienced[emotion] = st.session_state.moods_experienced.get(emotion, 0) + 1

    st.toast(
        f"Emotion changed to {emotion}",
        icon="✨"
    )


def detect_emotion_from_text(text: str, current_emotion: str) -> str:
    text_lower = text.lower()
    
    # Words indicating confusion
    confusion_keywords = [
        "confused", "stuck", "don't understand", "do not understand", "lost", "hard", 
        "difficult", "explain again", "what is", "how do", "clueless", "cannot get", 
        "can't get", "makes no sense", "unclear", "doubt", "explain step", 
        "puzzled", "confusing", "too fast", "slow down"
    ]
    
    # Words indicating engagement/practice request
    engagement_keywords = [
        "practice", "exercise", "question", "problem", "test me", "challenge", 
        "try", "engaged", "more examples", "solve", "quiz", "give me a"
    ]
    
    # Words indicating focus/understanding
    focus_keywords = [
        "understand", "got it", "makes sense", "clear", "focused", "easy", 
        "i see", "ah", "okay", "ok", "fine", "yes", "cool", "got clear"
    ]
    
    for word in confusion_keywords:
        if word in text_lower:
            return "confused"
            
    for word in engagement_keywords:
        if word in text_lower:
            return "engaged"
            
    for word in focus_keywords:
        if word in text_lower:
            return "focused"
            
    return current_emotion


def send_message(text):
    # Stop any active speaking playback
    st.session_state.currently_playing = None
    st.session_state.stop_speak = True

    # Increment chat interactions
    st.session_state.chat_interactions = st.session_state.get("chat_interactions", 0) + 1

    # Auto-detect emotion from text
    detected_emotion = detect_emotion_from_text(text, st.session_state.emotion)
    
    # Track mood history
    if "moods_experienced" in st.session_state:
        st.session_state.moods_experienced[detected_emotion] = st.session_state.moods_experienced.get(detected_emotion, 0) + 1

    if detected_emotion != st.session_state.emotion:
        st.session_state.emotion = detected_emotion
        st.toast(
            f"Auto-detected state: {detected_emotion.capitalize()}",
            icon="🤖"
        )

    st.session_state.chat_history.append(
        {
            "role": "user",
            "text": text,
            "badge": None
        }
    )

    with st.spinner("MindFlex AI is thinking..."):

        answer = ask_ai(
            question=text,
            emotion=st.session_state.emotion,
            notes=LESSONS[st.session_state.current_topic]["notes"]
        )

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "text": answer,
            "badge": (
                THEMES[st.session_state.emotion]["color"],
                f"Emotion: {st.session_state.emotion}"
            )
        }
    )


with st.sidebar:

    st.title("🧠 MindFlex AI")

    # Welcome card and learning analytics profile dashboard
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 12px; margin-bottom: 15px; text-align: center;">
            <span style="font-size: 11px; color: #9ca3af;">Student Profile:</span><br>
            <span style="font-size: 16px; font-weight: 700; color: #34d399;">{st.session_state.get('username', 'student').capitalize()} 🧑‍🎓</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Learning Analytics")
    
    # Calculate custom progress score
    total_interactions = st.session_state.get("chat_interactions", 0)
    labs_count = len(st.session_state.get("labs_explored", set()))
    tts_count = st.session_state.get("tts_reads", 0)
    
    progress_score = min(100, (total_interactions * 15) + (labs_count * 25) + (tts_count * 10))
    
    st.progress(progress_score / 100.0)
    st.caption(f"Engagement Score: **{progress_score}%**")
    
    # Mood Analytics
    moods = st.session_state.get("moods_experienced", {"focused": 1, "confused": 0, "engaged": 0})
    st.markdown(
        f"""
        <div style="font-size: 12px; color: #9ca3af; margin-bottom: 8px;">Tutor State Analytics:</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
            <span style="background: rgba(52, 211, 153, 0.08); color: #34d399; padding: 2px 6px; border-radius: 6px; font-size: 10px; font-weight: 600;">Focus: {moods.get('focused', 0)}</span>
            <span style="background: rgba(251, 191, 36, 0.08); color: #fbbf24; padding: 2px 6px; border-radius: 6px; font-size: 10px; font-weight: 600;">Confused: {moods.get('confused', 0)}</span>
            <span style="background: rgba(167, 139, 250, 0.08); color: #a78bfa; padding: 2px 6px; border-radius: 6px; font-size: 10px; font-weight: 600;">Engaged: {moods.get('engaged', 0)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Log Out 🔒", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

    # Render dynamic AI Tutor Avatar card
    current = THEMES[st.session_state.emotion]
    st.markdown(
        f"""
        <div class="avatar-card" style="box-shadow: 0 0 20px {current['glow']}; border-color: {current['color']}40;">
            <div class="avatar-emoji">{current['avatar']}</div>
            <div style="font-weight: 700; font-size: 16px; color: {current['color']};">Tutor Status: {current['name']}</div>
            <div class="avatar-status">{current['status']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Manual Override")

    st.button(
        "Focused 🟢",
        use_container_width=True,
        on_click=trigger_emotion,
        args=("focused",)
    )

    st.button(
        "Confused 🟠",
        use_container_width=True,
        on_click=trigger_emotion,
        args=("confused",)
    )

    st.button(
        "Engaged 🟣",
        use_container_width=True,
        on_click=trigger_emotion,
        args=("engaged",)
    )

    st.markdown("### LLM Configuration")

    st.selectbox(
        "LLM Provider:",
        ["🤖 Local Ollama", "⚡ Groq Cloud"],
        key="llm_provider"
    )

    if st.session_state.llm_provider == "⚡ Groq Cloud":
        st.text_input(
            "Groq API Key:",
            type="password",
            placeholder="gsk_...",
            key="groq_api_key",
            help="Get your free API key from https://console.groq.com/"
        )

    st.divider()

    if st.button("Reset Chat", use_container_width=True):

        st.session_state.chat_history = [
            {
                "role": "assistant",
                "text": "Hello! I am MindFlex AI. Ask me anything about today's lesson.",
                "badge": None
            }
        ]
        st.session_state.currently_playing = None
        st.session_state.stop_speak = True

        st.rerun()


current = THEMES[st.session_state.emotion]

st.markdown(
    f"""
    # 🧠 MindFlex AI
    **Current Emotion:** <span style='color:{current["color"]}'>{current["name"]}</span>
    """,
    unsafe_allow_html=True
)


left, right = st.columns([1, 2])


with left:

    st.subheader("📚 Lesson Modules")

    # Dynamic topic selector dropdown
    selected_topic = st.selectbox(
        "Choose Subject / Topic:",
        list(LESSONS.keys()),
        key="current_topic",
        on_change=lambda: st.toast("Switched to new learning module!", icon="📚")
    )

    lesson_data = LESSONS[selected_topic]

    st.write("Click on the steps below to expand the interactive walkthrough:")
    # Interactive collapsible accordion steps
    for step in lesson_data["steps"]:
        with st.expander(step["title"]):
            st.write(step["content"])

    # Topic-specific interactive play laboratory
    st.divider()
    st.subheader("🛠️ Concept Playground")

    if "Calculus" in selected_topic:
        show_sub = st.checkbox("Toggle Variable Substitution Swap")
        if show_sub:
            if "labs_explored" in st.session_state:
                st.session_state.labs_explored.add("calculus_swap")
            st.latex(r"\int 2x \cos(x^2) dx \quad \xrightarrow{u = x^2, \, du = 2x\,dx} \quad \int \cos(u) du")
            st.info("Substitution simplified the composite integral into a basic trigonometric form!")
        else:
            st.latex(r"\int 2x \cos(x^2) dx")
            st.caption("Check the box above to simulate the substitution swap step!")

    elif "Algebra" in selected_topic:
        st.write("Enter quadratic coefficients to test the discriminant solver:")
        c_a = st.number_input("a (quadratic coefficient)", value=1, step=1)
        c_b = st.number_input("b (linear coefficient)", value=-5, step=1)
        c_c = st.number_input("c (constant)", value=6, step=1)
        if c_a != 1 or c_b != -5 or c_c != 6:
            if "labs_explored" in st.session_state:
                st.session_state.labs_explored.add("algebra_solver")

        disc = c_b**2 - 4*c_a*c_c
        st.write(f"Discriminant $D = b^2 - 4ac$ = **{disc}**")
        if disc > 0:
            st.success("Two distinct real roots exist.")
        elif disc == 0:
            st.warning("Exactly one real root exists.")
        else:
            st.error("No real roots exist (roots are complex numbers).")

    elif "Physics" in selected_topic:
        st.write("Adjust mass and velocities to calculate kinetic energy net work:")
        p_mass = st.slider("Object Mass (kg)", 1, 10, 2)
        p_vi = st.slider("Initial Velocity (m/s)", 0, 10, 2)
        p_vf = st.slider("Final Velocity (m/s)", 0, 20, 6)
        if p_mass != 2 or p_vi != 2 or p_vf != 6:
            if "labs_explored" in st.session_state:
                st.session_state.labs_explored.add("physics_calculator")

        k_i = 0.5 * p_mass * (p_vi**2)
        k_f = 0.5 * p_mass * (p_vf**2)
        work_done = k_f - k_i

        st.metric(label="Initial Kinetic Energy", value=f"{k_i} J")
        st.metric(label="Final Kinetic Energy", value=f"{k_f} J")
        st.metric(label="Net Work Done (W_net)", value=f"{work_done} Joules")


with right:

    st.subheader("💬 Adaptive Tutor")

    chat_container = st.container(height=450)

    with chat_container:

        for i, msg in enumerate(st.session_state.chat_history):

            # Use cute emoji avatars to avoid offline Material Icon loading issues (e.g., 'art_')
            avatar_emoji = "🤖" if msg["role"] == "assistant" else "🧑‍🎓"

            with st.chat_message(msg["role"], avatar=avatar_emoji):

                st.markdown(msg["text"])

                badge_col, speak_col = st.columns([9, 1])

                with badge_col:
                    if msg["badge"]:
                        color, badge_text = msg["badge"]
                        st.markdown(
                            f"""
                            <div class="badge"
                                 style="border:1px solid {color};
                                 color:{color};">
                                 {badge_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                with speak_col:
                    if msg["role"] == "assistant":
                        is_playing = st.session_state.get("currently_playing") == i
                        button_label = "🔇" if is_playing else "🔊"
                        button_help = "Stop reading aloud" if is_playing else "Read aloud"
                        
                        if st.button(button_label, key=f"speak_{i}", help=button_help):
                            if is_playing:
                                st.session_state.currently_playing = None
                                st.session_state.stop_speak = True
                            else:
                                import re
                                st.session_state.tts_reads = st.session_state.get("tts_reads", 0) + 1
                                # Clean up markdown markers for speech synthesis
                                clean_text = re.sub(r'[*#_`\-]', ' ', msg["text"])
                                # Strip double spaces and LaTeX syntax
                                clean_text = re.sub(r'\\\(|\\\)|\\\[|\\\]', ' ', clean_text)
                                st.session_state.speak_text = clean_text
                                st.session_state.currently_playing = i
                                if "stop_speak" in st.session_state:
                                    del st.session_state.stop_speak
                            st.rerun()

    st.markdown("### Quick Questions")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Explain Step 3",
            use_container_width=True
        ):
            send_message("Explain Step 3")
            st.rerun()

    with c2:
        if st.button(
            "I am confused",
            use_container_width=True
        ):
            send_message("I am confused about substitution")
            st.rerun()

    with c3:
        if st.button(
            "Practice Problem",
            use_container_width=True
        ):
            send_message("Give me a practice problem")
            st.rerun()

    prompt = st.chat_input(
        "Ask MindFlex AI..."
    )

    if prompt:

        send_message(prompt)

        st.rerun()


# --- Speech Synthesis Player ---
if "speak_text" in st.session_state and st.session_state.speak_text:
    escaped_text = st.session_state.speak_text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    st.components.v1.html(
        f"""
        <script>
            if ('speechSynthesis' in window.parent) {{
                window.parent.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance("{escaped_text}");
                utterance.rate = 1.05;
                window.parent.speechSynthesis.speak(utterance);
            }}
        </script>
        """,
        height=0,
        width=0
    )
    st.session_state.speak_text = ""

if st.session_state.get("stop_speak"):
    st.components.v1.html(
        """
        <script>
            if ('speechSynthesis' in window.parent) {
                window.parent.speechSynthesis.cancel();
            }
        </script>
        """,
        height=0,
        width=0
    )
    st.session_state.stop_speak = False