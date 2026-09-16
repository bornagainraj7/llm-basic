import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from llm_client import get_llm_response
print()
print("========================= Stateful LLM Client (With memory) =========================")
print()

# Initialize an empty list to store the conversation history
conversation_history = []

while True: 
    user_input = input("User Prompt: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    conversation_history.append({"role": "user", "content": user_input})
    # message = conversation_history # appending complete conversation history to the message list
    MAX_HISTORY_LENGTH = 6
    conversation_history = conversation_history[-MAX_HISTORY_LENGTH:]

    response_text = get_llm_response(conversation_history, provider="openai")
    conversation_history.append({"role": "assistant", "content": response_text})
    print(f"AI Response: {response_text}")
    print()

