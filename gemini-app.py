import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai as gemini


load_dotenv(Path(__file__).resolve().parent / ".env") 


client = gemini.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# for model in client.models.list():
# 	print(model.name)

prompt_message = "Write a short beginner friendly explanation of LLM in 200 words."

# You'll get AFC warning using this method 
# Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. 
# Instead, we recommend to use AFC in Chat.send_message. 
# Similarly, direct use of AFC in Models.generate_content_stream is not recommended. 
# Instead, we recommend to use AFC in Chat.send_message_stream.

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt_message,
)

# print(response)
# print("")
print(f"User Prompt: {prompt_message}")
print(f"AI Response: {response.text}")