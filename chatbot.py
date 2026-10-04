import urllib.request
import json

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

print("Chatbot started. Type 'quit' to exit.")
print("-" * 40)

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    # Prepare the request
    url = "http://127.0.0.1:11434/api/chat"
    data = json.dumps({
        "model": "llama3.2:3b",
        "messages": messages,
        "stream": False
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            reply = result["message"]["content"]
            print(f"AI: {reply}")
            print("-" * 40)
            messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Ollama desktop app is running (look for the llama icon near the clock).")
        break