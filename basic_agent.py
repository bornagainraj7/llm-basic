import json
from llm_client import get_llm_response
import random

print("================================ Basic Multi-tool AI Agent ================================")
print("\n Type 'exit' or 'quit' to end the conversation \n")

# Tools

def get_weather(city):
    weather_options = [
        f"The weather in {city} is clam and pleasant with 25*C",
        f"Weather in {city} today is hot and humid with 32*C",
        f"Its rainy out there in {city} with 21*C"
    ]

    final = random.choice(weather_options)
    return final

def suggest_activity(weather):
    if "hot" in weather.lower():
        return "You can take a walk in the evening."
    elif "pleasant" in weather or "25" in weather:
        return "Its a awesome day for outdoor workout, go for a run."
    else:
        return "Try doing indoor activities such as HIIT."

def calorie_estimates(activity):
    if "run" in activity.lower():
        return "Your estimated calorie burn for a run should be around 120-150 Kcal"
    elif "hiit" in activity.lower():
        return "Your estimated calorie burn for a HIIT should be around 170-200 Kcal"
    else:
        return "Your estimated calorie burn for a evening walk should be around 50 Kcal"


TOOLS = {
    "weather": get_weather,
    "activity": suggest_activity,
    "calorie": calorie_estimates
}


SYSTEM_PROMPT = """
You're an intelligent planning agent

You must solve the user's problem step by step using tools provided below.

Available Tools:
1. weather(city)
2. activity(weather)
3. calorie(activity)

Rules:
- Think step by step
- Use tools when needed
- You can call multiple tools in sequence
- You must go through all steps in sequence
- Use previous results to decide next step
- You must respond based on the results received from each tool callings and their response
- if the answer of previous activity is present, it will be provide as "Result of {tool}: {result}" format, 
you need to use this result to call next tool

Respond only in JSON format

step format:
{
    "action": "tool_name",
    "input": "input"
}

Final output format:
{
    "final_output": "complete answer"
}
Do not use markdown for answer
"""
# adding below line usually crashes
# You have to go through all the tools in sequence


# conversation loop
while True:
    user_input = input("\nUser Input: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    context = user_input
    step = 1

    while True:
        print(f"\n-------------- Step {step}: --------------")

        message = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ]

        response_text = get_llm_response(message, provider='lmstudio')
        print(f"\nAgent Decision: {response_text}")

        clean = response_text.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(clean)
            if "final_output" in data:
                print(f"\nActivity Plan: \n{data['final_output']}\n") 
                break

            # tool calling
            action = data.get("action")
            tool_input = data.get("input", "")

            if action in TOOLS:
                print(f"Using tool: {action}, with input: {tool_input}")   

                result = TOOLS[action](tool_input)
                print(f"Response from tool: {action}, was response: {result}")

                context += f"\nResult of {action}: {result}" 

            else:
                print(f"\nUnknown Tool: {action}\n")
                break
        except:
            print("Failed to parse response for clear json\n\n")
            break

        step += 1


