import json
from datetime import datetime
from llm_client import get_llm_response

print("============================= Tool enabled chatbot =============================")
print("\nType 'exit' or 'quit' to end the conversation\n")


# Step 1: Define tools

def calculator(exp):
    try:
        return str(eval(exp))
    except:
        return "Invalid expression"

def get_weather(city):
    return f"The weather in {city} is 25*C clear and sunny"

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Step 2: Tools registry
TOOLS = {
    "calculator": calculator,
    "weather": get_weather,
    "time": get_current_time,
    "date": get_current_time
}


# Step 3: System prompt
SYSTEM_PROMPT = """
You're an AI assistant, with access to tools.
Below are the available tools:
1. calculator: for math expressions
2. weather: get weather of provided location/city
3. time: get current time
4. date: get current date

When a tool is needed, response only in JSON format as below:
{
    "tool": "tool_name",
    "input": "input_for_tool"
}

NOTE: If no tool calling is needed, response as a general LLM Agent.
"""

# Step 4: Conevrsation loop

while True:
    user_input = input("\nUser prompt: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\n Exiting...")
        break

    message = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": user_input }
    ]

    response_text = get_llm_response(message, provider="gemini")
    print(f"\nRaw response: {response_text}\n") 

    clean_response = response_text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(clean_response)

        tool = data["tool"]
        tool_input = data.get("input", "")

        if tool in TOOLS:
            print(f"\n Using Tool: {tool}")
            result = TOOLS[tool](tool_input) if tool_input else TOOLS[tool]()
            print(f"\nTool result: {result}")
            # asking LLM for final answer
            final_response_text = get_llm_response([
                { "role": "user", "content": f"User asked: {user_input}\n Tool result: {result}" }
            ])

            print(f"AI's final response: {final_response_text}")
        else:
            print(f"AI's response: {response_text}")

    except:
        print(f"AI response: {response_text}")

