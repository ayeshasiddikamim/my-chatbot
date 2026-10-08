import json
import urllib.request
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

app = FastAPI()

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2:3b"

class ChatRequest(BaseModel):
    message: str
    history: list = []
    personality: str = "assistant"
@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    personalities = {
        "assistant": "You are a helpful AI assistant.",
        "tutor": "You are a patient programming tutor. Explain things step by step with simple examples.",
        "interviewer": "You are a technical interviewer. Ask the user questions, evaluate their answers, and give constructive feedback.",
        "reviewer": "You are a senior code reviewer. Analyze code the user shares, point out bugs, suggest improvements, and be specific."
    }
    system_prompt = personalities.get(req.personality, personalities["assistant"])
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(req.history)
    messages.append({"role": "user", "content": req.message})

    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": True
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    def stream_response():
        try:
            with urllib.request.urlopen(request) as response:
                for line in response:
                    if line.strip():
                        chunk = json.loads(line.decode("utf-8"))
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield content
        except Exception as e:
            yield f"\n[Error: {e}]"

    return StreamingResponse(stream_response(), media_type="text/plain")