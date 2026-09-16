import os


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from google import genai as gemini


def get_llm_response(message, provider=None):
    provider = provider or os.getenv("PROVIDER", "gemini")

    if provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model_name = "gpt-5-nano"
        messages=[]

        for m in message:
            role  = m["role"]
            content = m["content"]
            item = {"role": role, "content": content}
            messages.append(item)

        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        return response.choices[0].message.content
    elif provider == "gemini":
        gemini_client = gemini.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        model_name = "gemini-3.5-flash-lite"
        chat = gemini_client.chats.create(model=model_name)

        prompt = ""

        for m in message: 
            role = m["role"]
            content = m["content"]
            prompt += f"{role}: {content}\n"

        return chat.send_message(prompt).text

        # different approach
        # response = gemini_client.models.generate_content(
        #     model=model_name,
        #     contents=prompt
        # )
        # return response.text
    elif provider in ["local", "lmstudio", "ollama"]:
        local_client = OpenAI(
            base_url=f"http://localhost:1234/v1/",
            api_key="lm-studio",
        )
        # model_name = os.getenv("LM_STUDIO_MODEL", "deepseek-r1_8b") # ok ok, taking too much time to respond
        # model_name = os.getenv("LM_STUDIO_MODEL", "llama-3.2-3b") # bad response from model
        model_name = os.getenv("LM_STUDIO_MODEL", "gemma-4-e4b-it-qat") # good and fast response


        messages = []

        for m in message:
            role = m["role"]
            content = m["content"]
            messages.append({ "role": role, "content": content })

        response = local_client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        return response.choices[0].message.content
    else:
        raise ValueError(f"Unsupported provider: {provider}")