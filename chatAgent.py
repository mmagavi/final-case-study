import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_response(user_input: str, system_content: str, information: str):
# Make a chat request
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "system", "content": information},
            {"role": "user", "content": user_input}
        ]
    )

    # Check if the response contains choices and is not empty
    if not response.choices:
        return("Error: No response from the model")

    return response.choices[0].message.content