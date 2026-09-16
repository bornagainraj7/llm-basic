import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from llm_client import get_llm_response

print("========================= Basic Chatbot (No external knowledge) =========================")   
print()
print("Type 'exit' or 'quit' to end the conversation.\n")

system_prompt = """
You are a helpful assistant.
If you do not know the answer, still try to answer anyway. 
Make sure answer are to the point and concise.
"""
message = []

while True:
    user_input = input("User Prompt: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    message.append({ "role": "system", "content": system_prompt })
    message.append({ "role": "user", "content": user_input })
    # message = message[-3:]  # Keep only the last 3 messages (system, user, assistant)
    response_text = get_llm_response(message, provider="gemini")
    message.append({ "role": "assistant", "content": response_text })
    print(f"AI Response: {response_text}")
    print("", "\n\n")