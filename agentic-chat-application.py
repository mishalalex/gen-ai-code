import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Set up Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use Gemini's free model
model = genai.GenerativeModel("gemini-2.5-flash")

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolving the user query.

For the given user input, analyse the input and break down the problem step by step.
At least think 5-6 steps on how to solve the problem before solving it.

The steps are: "analyse", "think", "output", "validate", and finally "result".

Rules:
1. Follow the strict JSON output schema.
2. Always perform one step at a time and wait for the next input.
3. Carefully analyse the user query.

✅ Output Format (strict JSON):
{ "step": "string", "content": "string" }

🧪 Example:
Input: What is 2 + 2.
Output: { "step": "analyse", "content": "The user is interested in a basic arithmetic question: 2 + 2." }
Output: { "step": "think", "content": "To perform the addition, I need to add 2 and 2." }
Output: { "step": "output", "content": "4" }
Output: { "step": "validate", "content": "The result of 2 + 2 is indeed 4." }
Output: { "step": "result", "content": "2 + 2 = 4" }
"""
# Start a chat session with Gemini
chat = model.start_chat(
    history=[
    {"role": "user", "parts": [system_prompt]}
])

# Take user query
query = input("> ")
chat.send_message(query)

while True:
    if(query=="exit"):
        print("Alright. That's my time. Have a good day everyone!")
        break
    response = chat.last.text.strip()

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        print("⚠️ Warning: Response was not in valid JSON format. Full response below ⚠️:")
        print(response)
        break

    # Append response back to chat history
    chat.send_message(json.dumps(parsed))

    step = parsed.get("step")
    content = parsed.get("content")

    if step != "output":
        print(f"🧠: {content}")
        continue

    print(f"🤖: {content}")
    break
