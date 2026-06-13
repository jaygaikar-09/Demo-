import streamlit as st
import requests


st.set_page_config(
    page_title="MindFlex AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/chat"

LESSON_NOTES = """
Topic: Calculus - Integration by Substitution

Goal:
Simplify integrals of composite functions.

Step 1: Choose a substitution u = g(x)
Step 2: Find du = g'(x)dx
Step 3: Substitute into the integral
Step 4: Integrate with respect to u
Step 5: Replace u with g(x)

Example:
∫ 2x cos(x²) dx

Let:
u = x²
du = 2x dx

Integral becomes:
∫ cos(u) du
"""


st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #020617;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #0f172a;
}

.badge {
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 8px;
    display: inline-block;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)


if "emotion" not in st.session_state:
    st.session_state.emotion = "focused"

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
        "color": "#34d399"
    },
    "confused": {
        "name": "Confused 🟠",
        "color": "#fbbf24"
    },
    "engaged": {
        "name": "Engaged 🟣",
        "color": "#a78bfa"
    }
}


def ask_ai(question, emotion, notes):

    payload = {
        "question": question,
        "emotion": emotion,
        "lesson_notes": notes
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            return response.json()["response"]

        return f"Backend Error: {response.text}"

    except Exception as e:
        return f"Connection Error: {str(e)}"


def trigger_emotion(emotion):

    st.session_state.emotion = emotion

    st.toast(
        f"Emotion changed to {emotion}",
        icon="✨"
    )


def send_message(text):

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
            notes=LESSON_NOTES
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

    st.markdown("### Emotion Controls")

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

    st.divider()

    if st.button("Reset Chat", use_container_width=True):

        st.session_state.chat_history = [
            {
                "role": "assistant",
                "text": "Hello! I am MindFlex AI. Ask me anything about today's lesson.",
                "badge": None
            }
        ]

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

    st.subheader("📚 Lesson Notes")

    st.code(
        LESSON_NOTES,
        language="python"
    )


with right:

    st.subheader("💬 Adaptive Tutor")

    chat_container = st.container(height=450)

    with chat_container:

        for msg in st.session_state.chat_history:

            with st.chat_message(msg["role"]):

                st.markdown(msg["text"])

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