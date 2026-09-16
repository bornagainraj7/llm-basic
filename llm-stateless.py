import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from llm_client import get_llm_response
print()
print("========================= Stateless LLM Client (No memory) =========================")
print()

while True:
    user_input = input("User Prompt: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    message = [{"role": "user", "content": user_input}]
    response_text = get_llm_response(message, provider="openai")

    print(f"AI Response: {response_text}")
    print()

