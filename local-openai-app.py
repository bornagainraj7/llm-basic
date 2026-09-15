import os

import lmstudio
from openai import OpenAI


lmstudio_host = os.getenv("LM_STUDIO_HOST", "192.168.56.1:1234")
lmstudio_host = lmstudio_host.removeprefix("http://").removeprefix("https://").rstrip("/")

lmstudio_client = lmstudio.Client(api_host=lmstudio_host)

for loaded_model in lmstudio_client.list_loaded_models():
	print(f"Unloading model: {loaded_model}")
	loaded_model.unload()


client = OpenAI(
	base_url=f"http://{lmstudio_host}/v1/",
	api_key="lm-studio",
)

prompt = "Write a short beginner friendly explanation of LLM in 200 words."

models = client.models.list()

# get model list
# for model in models:
#     print(model.id)

model_name = os.getenv("LM_STUDIO_MODEL", "deepseek-r1_8b")

response = client.chat.completions.create(
	model=model_name,
	messages=[
		{"role": "user", "content": prompt},
	],
)

print(f"User Prompt: {prompt}")
print(f"AI Response: {response.choices[0].message.content}")