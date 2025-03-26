# %%
import os
from dotenv import load_dotenv
from ai21 import AI21Client
from ai21.models.chat.chat_message import AssistantMessage, SystemMessage, UserMessage

load_dotenv()

AI21_KEY = os.getenv('AI21_KEY')

# %%
client = AI21Client(
    api_key = AI21_KEY
)

system = "You're a bot assistant"

messages = [
    SystemMessage(content=system, role="system"),
    UserMessage(content="Hello, how can you help me?", role="user")
]

def chat(user_input):
    messages.append(UserMessage(content=user_input, role="user"))

    chat_response = client.chat.completions.create(
        system=system,
        messages=messages,
        model="jamba-mini",
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
        stop=["\n"],
        stream=True
    )

    full_response = []

    for chunk in chat_response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)  
            full_response.append(content)

    
    assistant_response = "".join(full_response)
    messages.append(AssistantMessage(content=assistant_response, role="assistant"))
    print('\n')
    
    return assistant_response
# %%
while True:
    user_input = input('input: ')
    if user_input.lower() == 'exit':
        break
    chat(user_input)
# %%
