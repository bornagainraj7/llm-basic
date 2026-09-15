import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai as gemini

load_dotenv()

client = gemini.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

prompt_message = "Write a short beginner friendly explanation of LLM in 200 words."
chat = client.chats.create(model="gemini-3.5-flash-lite")
response = chat.send_message(prompt_message)

print(f"User Prompt: {prompt_message}")
print(f"AI Response({client.models.get(model='gemini-3.5-flash-lite').name}): {response.text}")