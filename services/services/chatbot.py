import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_bot_response(user_message, conversation_history=[]):
    system_prompt = {"role": "system", "content": "You are a helpful travel and safety assistant."}
    messages = [system_prompt] + conversation_history + [{"role": "user", "content": user_message}]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content
