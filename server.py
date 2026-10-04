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

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
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