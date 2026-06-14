from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import traceback

# ✅ IMPORT OLLAMA
import ollama
from ollama import AsyncClient

# ---------------- OLLAMA LLM ----------------
# (CrewAI imports and setup kept commented out for reference)
# from crewai import LLM, Crew, Agent, Task
# llm = LLM(
#     model="ollama/qwen2.5:3b",
#     base_url="http://localhost:11434"
# )

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CREW BUILDER (BYPASSED FOR SPEED) ----------------
# def build_crew(data):
# 
#     agent = Agent(
#         role="AI Tutor",
#         goal="Teach concepts in a simple and clear way",
#         backstory="You are a friendly teacher who explains step-by-step",
#         llm=llm,   # 🔥 IMPORTANT FIX: attach LLM here
#         verbose=True
#     )
# 
#     task = Task(
#         description=f"""
#         Student Question: {data.get('question')}
#         Student Emotion: {data.get('emotion')}
#         Lesson Notes: {data.get('lesson_notes')}
# 
#         Explain step by step in simple language with examples.
#         """,
#         expected_output="""
#         A clear, beginner-friendly explanation with steps and examples.
#         """,
#         agent=agent
#     )
# 
#     return Crew(
#         agents=[agent],
#         tasks=[task],
#         verbose=True
#     )


# ---------------- CHAT ENDPOINT ----------------
@app.post("/chat")
def chat(data: dict):

    try:
        if not data.get("question"):
            return {"error": "Question is required"}

        # Construct a direct and concise prompt for Ollama based on student emotion
        emotion = data.get("emotion", "focused").lower()
        lesson_notes = data.get("lesson_notes", "")

        if emotion == "confused":
            system_instruction = (
                "You are an AI Tutor, a highly supportive, patient and encouraging teacher. "
                "The student is currently CONFUSED. Your absolute priority is to simplify. "
                "1. Start with supportive words (e.g., 'No worries, let's break this down together!').\n"
                "2. Use real-world analogies (e.g., comparing substitution to swapping labels or unpacking nested boxes).\n"
                "3. Avoid using overly dense mathematical terminology where simple words work.\n"
                "4. Keep explanations short, simple, and step-by-step. Avoid huge walls of text.\n"
                "5. End with a simple, encouraging question to check if they understand the first step.\n\n"
                f"Lesson Notes:\n{lesson_notes}"
            )
            user_prompt = (
                f"Student Question: {data.get('question')}\n\n"
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
                f"Lesson Notes:\n{lesson_notes}"
            )
            user_prompt = (
                f"Student Question: {data.get('question')}\n\n"
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
                f"Lesson Notes:\n{lesson_notes}"
            )
            user_prompt = (
                f"Student Question: {data.get('question')}\n\n"
                "Explain step by step with clear math formatting and point out common edge cases."
            )

        response = ollama.Client(host="http://127.0.0.1:11434").chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )

        return {
            "response": response["message"]["content"]
        }

    except Exception as e:
        print("🔥 BACKEND ERROR:\n", traceback.format_exc())

        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }