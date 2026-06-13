from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import traceback

# ✅ IMPORT LLM (IMPORTANT FIX)
from crewai import LLM, Crew, Agent, Task

# ---------------- OLLAMA LLM ----------------
llm = LLM(
    model="ollama/qwen2.5:3b",
    base_url="http://localhost:11434"
)

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CREW BUILDER ----------------
def build_crew(data):

    agent = Agent(
        role="AI Tutor",
        goal="Teach concepts in a simple and clear way",
        backstory="You are a friendly teacher who explains step-by-step",
        llm=llm,   # 🔥 IMPORTANT FIX: attach LLM here
        verbose=True
    )

    task = Task(
        description=f"""
        Student Question: {data.get('question')}
        Student Emotion: {data.get('emotion')}
        Lesson Notes: {data.get('lesson_notes')}

        Explain step by step in simple language with examples.
        """,
        expected_output="""
        A clear, beginner-friendly explanation with steps and examples.
        """,
        agent=agent
    )

    return Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )


# ---------------- CHAT ENDPOINT ----------------
@app.post("/chat")
async def chat(request: Request):

    try:
        data = await request.json()

        if not data.get("question"):
            return {"error": "Question is required"}

        crew = build_crew(data)

        # ✅ async execution
        result = await crew.kickoff_async()

        return {
            "response": str(result)
        }

    except Exception as e:
        print("🔥 BACKEND ERROR:\n", traceback.format_exc())

        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }