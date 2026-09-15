import lmstudio as lms

model = lms.llm()
prompt = "Write a short beginner friendly explanation of LLM in 200 words."
response = model.respond(prompt)

print(f"User Prompt: {prompt}") 
print(f"AI Response: {response}")