import streamlit as st
import time

# --- Page Configuration & Theming ---
st.set_page_config(page_title="MindFlex AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS to mimic Tailwind Slate-900 dark mode and neon glow
st.markdown("""
<style>
    /* Base Theme */
    [data-testid="stAppViewContainer"] {
        background-color: #020617; /* slate-950 */
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a; /* slate-900 */
        border-right: 1px solid #1e293b;
    }
    [data-testid="stHeader"] { background-color: transparent; }
    
    /* Webcam Mock Animations & Styling */
    .webcam-container {
        position: relative;
        height: 250px;
        background-color: #0f172a;
        background-image: url('https://images.unsplash.com/photo-1516321497487-e288fb19713f?q=80&w=600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
        border: 1px solid #1e293b;
        border-radius: 1rem;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .bounding-box {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 180px; height: 180px;
        border: 2px dashed;
        border-radius: 0.75rem;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: .5; }
    }
    .overlay-stats {
        position: absolute;
        bottom: 10px; left: 10px; right: 10px;
        background: rgba(2, 6, 23, 0.9);
        border: 1px solid #1e293b;
        border-radius: 0.5rem;
        padding: 8px;
        font-family: monospace;
        font-size: 0.8rem;
    }
    
    /* Chat Badges */
    .badge {
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 6px;
        margin-top: 8px;
        display: inline-block;
        border: 1px solid;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'emotion' not in st.session_state:
    st.session_state.emotion = 'focused'

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{
        "role": "assistant",
        "text": "Welcome back, Somya! 🌟 We're continuing our review of Integration techniques today. How are you feeling about u-substitution so far?",
        "badge": None
    }]

# --- Emotion Themes ---
THEMES = {
    'focused': {
        'color': '#34d399', 'name': 'Focused (🟢)', 'border': 'border-emerald-400',
        'stats': {'eng': '85%', 'conf': '5%', 'foc': 'High'},
        'message': 'Switched to Normal/Focused mode.'
    },
    'confused': {
        'color': '#fbbf24', 'name': 'Confused (🟠)', 'border': 'border-amber-400',
        'stats': {'eng': '45%', 'conf': '78%', 'foc': 'Medium'},
        'message': 'Simulating user confusion...'
    },
    'engaged': {
        'color': '#a78bfa', 'name': 'Highly Engaged (🟣)', 'border': 'border-violet-400',
        'stats': {'eng': '98%', 'conf': '2%', 'foc': 'Flow State'},
        'message': 'Simulating high engagement flow!'
    }
}
current_theme = THEMES[st.session_state.emotion]

# --- Handlers ---
def trigger_emotion(new_emotion):
    st.session_state.emotion = new_emotion
    st.toast(THEMES[new_emotion]['message'], icon='✨') # Added user-friendly toast feedback
    
    # Simulate AI adaptive response based on triggered emotion
    if new_emotion == 'confused':
        st.session_state.chat_history.append({
            "role": "assistant",
            "text": "I noticed you might be hesitating. Let's step back: Instead of thinking about the math formula, imagine 'u' as a container. We are putting a messy part of the equation into a neat box to make it easier to handle. Does that visual help?",
            "badge": ("#fbbf24", "💡 AI Adapted: Simpler Analogy triggered by Confusion")
        })
    elif new_emotion == 'engaged':
        st.session_state.chat_history.append({
            "role": "assistant",
            "text": "You're tracking this perfectly! Since you're highly engaged, let's look at a more complex edge case: what happens when the derivative isn't a perfect match for 'du'?",
            "badge": ("#a78bfa", "🚀 AI Increased Depth: Advanced Topic triggered by High Engagement")
        })

def send_quick_message(text):
    st.session_state.chat_history.append({"role": "user", "text": text, "badge": None})
    st.session_state.chat_history.append({
        "role": "assistant",
        "text": "I'm processing that based on your current lesson structure... (Backend API connects here)",
        "badge": None
    })

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🧠 MindFlex.ai")
    st.radio("Navigation Menu", ["Dashboard", "AI Tutor", "Progress Analytics", "Settings"], index=1, label_visibility="collapsed")
    
    st.divider()
    
    st.markdown("#### 🛠️ Prototype Controls")
    st.caption("Click below to test how the AI adapts to Somya's different emotional states:")
    st.button("Normal / Focused 🟢", on_click=trigger_emotion, args=('focused',), use_container_width=True, help="Sets the baseline learning state.")
    st.button("Trigger Confusion 🟠", on_click=trigger_emotion, args=('confused',), use_container_width=True, help="Prompts the AI to simplify its explanation.")
    st.button("Trigger Engagement 🟣", on_click=trigger_emotion, args=('engaged',), use_container_width=True, help="Prompts the AI to introduce advanced topics.")
    
    st.divider()
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.chat_history = [{
            "role": "assistant",
            "text": "Welcome back, Somya! 🌟 We're continuing our review of Integration techniques today. How are you feeling about u-substitution so far?",
            "badge": None
        }]
        st.session_state.emotion = 'focused'
        st.rerun()

# --- Top Header ---
col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
with col_h1:
    st.markdown(f"## Integration Mastery <span style='font-size:1rem; color:{current_theme['color']}; border: 1px solid {current_theme['color']}; padding: 6px 14px; border-radius: 20px; margin-left:15px; vertical-align: middle;'>Current Mood: {current_theme['name']}</span>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align: right; margin-top: 10px; color:#f97316; font-size: 1.1rem;'>🔥 <b>12 Day Streak</b></div>", unsafe_allow_html=True)
with col_h3:
    st.markdown("<div style='text-align: right; margin-top: 10px; font-size: 1.1rem;'>👤 <b>Somya</b></div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color: #1e293b; margin-top: 0;'>", unsafe_allow_html=True)

# --- Main Workspace Split ---
left_col, right_col = st.columns([1, 1.8], gap="large")

# --- Left Panel: Camera & Notes ---
with left_col:
    # Webcam Mock using HTML/CSS
    st.markdown(f"""
    <div class="webcam-container">
        <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); padding: 4px 10px; border-radius: 5px; font-size: 0.75rem; font-weight: bold; color: #cbd5e1; letter-spacing: 1px;">🔴 LIVE_ANALYSIS</div>
        
        <div class="bounding-box" style="border-color: {current_theme['color']}; box-shadow: 0 0 15px {current_theme['color']};"></div>
        
        <div class="overlay-stats">
            <div style="display: flex; justify-content: space-between; margin-bottom: 2px;"><span>Engagement:</span> <span style="color: {current_theme['color']}; font-weight: bold;">{current_theme['stats']['eng']}</span></div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 2px;"><span>Confusion:</span> <span style="color: {current_theme['color']}; font-weight: bold;">{current_theme['stats']['conf']}</span></div>
            <div style="display: flex; justify-content: space-between;"><span>Focus:</span> <span style="color: {current_theme['color']}; font-weight: bold;">{current_theme['stats']['foc']}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Lesson Notes
    st.markdown("##### 📝 Live Lesson Notes")
    lesson_notes = """// Topic: Calculus - Integration by Substitution
// Goal: Simplify integrals of composite functions.

Step 1: Choose a substitution u = g(x)
Step 2: Find du = g'(x) dx
Step 3: Substitute into the integral
Step 4: Integrate with respect to u
Step 5: Replace u with g(x)

Example: ∫ 2x * cos(x^2) dx
Let u = x^2, then du = 2x dx.
Integral becomes: ∫ cos(u) du"""
    st.code(lesson_notes, language="python")

# --- Right Panel: Adaptive Chat ---
with right_col:
    # Create a container for the chat history to keep it visually contained
    chat_container = st.container(height=430)
    
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["text"])
                # Render adaptive badges if they exist
                if msg["badge"]:
                    color, text = msg["badge"]
                    st.markdown(f"<div class='badge' style='color:{color}; border-color:{color}; background:rgba(0,0,0,0.2);'>{text}</div>", unsafe_allow_html=True)

    # Quick Reply Suggestions (Highly User Friendly)
    st.markdown("<p style='font-size: 0.8rem; color: #94a3b8; margin-bottom: 5px;'>Quick Questions:</p>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        st.button("Can you explain Step 3?", on_click=send_quick_message, args=("Can you explain Step 3 again?",), use_container_width=True)
    with q_col2:
        st.button("I think I'm lost...", on_click=send_quick_message, args=("I think I'm completely lost right now.",), use_container_width=True)
    with q_col3:
        st.button("Give me a practice problem.", on_click=send_quick_message, args=("I'm ready. Give me a practice problem.",), use_container_width=True)

    # Main Chat Input
    if prompt := st.chat_input("Or type your own question here..."):
        send_quick_message(prompt)
        st.rerun()