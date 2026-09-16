import os


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_message = "Write a short beginner friendly explanation of LLM in 200 words."
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "user", "content": prompt_message}
    ]
)

print(f"User Prompt: {prompt_message}")
print(f"AI Response ({response.model}): {response.choices[0].message.content}")
