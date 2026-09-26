
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from task_parser import parse_task
from planner import create_plan
from browser_agent import execute_plan
from pii_detector import detect_pii
from pii_handler import redact_pii


app = FastAPI(
    title="Veil Browser Agent",
    description="Task Understanding and Execution API",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    instruction: str


class PageState(BaseModel):
    url: str
    title: str
    text: str


@app.get("/")
def home():
    return {
        "message": "Veil Browser Agent is running"
    }


@app.post("/task")
def understand_task(request: TaskRequest):
    result = parse_task(request.instruction)

    return {
        "status": "success",
        "message": "Task understood",
        "task": result
    }


@app.post("/execute")
def execute_task(request: TaskRequest):
    try:
        # 1. Understand the user's instruction.
        task = parse_task(request.instruction)

        # 2. Generate browser action plan.
        plan = create_plan(task)

        # 3. Execute plan and verify final result.
        results = execute_plan(plan)

        return {
            "status": "completed",
            "task": task,
            "plan": plan,
            "results": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/page-state")
def receive_page_state(page: PageState):
    # Detect and mask visible page text locally.
    pii = detect_pii(page.text)
    safe_text = redact_pii(page.text, pii)

    # Avoid printing the original page text.
    print("Received page state.")
    print("URL:", page.url)
    print("Title:", page.title)
    print("PII detected:", pii)
    print("Safe text:", safe_text[:500])

    return {
        "status": "success",
        "message": "Page state received",
        "pii_detected": pii,
        "safe_text": safe_text
    }