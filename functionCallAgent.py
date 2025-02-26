import openai
import os
from dotenv import load_dotenv
from agents.utils import get_availability_util, get_pricing_util, get_hours_util, get_image_util, use_part_util
import json

load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)



# Make a chat request
def make_chat_request(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are a helpful assistant for a pool parts business. You answer user queries related to pool equipment, store details, and product information. 
             If a user asks about something unrelated, you apologize and tell them you cannot answer their question. You don't need to use tools unless it is necessary"""},
            {"role": "user", "content": user_input}
        ],
        tools = [
            { "type": "function",
             "function": {
                 "name": "get_availability_util",
                "description": "Get the availability of an item",
                "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                    "type": "string",
                    "description": "The item"
                    },
                    "need_item_code": {
                    "type": "boolean",
                    "description": "boolean describing whether the user provided the item code or item name. True if the user provided the name, false if teh user provided the code."
                    },
                    "unit": {
                    "type": "string",
                    "description": "The number of items to check for - defaults to 1"
                    }
                },
                "required": ["item", "need_item_code"]
                }
            }},
            { "type": "function",
             "function": {
                 "name": "get_pricing_util",
                "description": "Get the pricing of an item",
                "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                    "type": "string",
                    "description": "The item"
                    },
                    "need_item_code": {
                    "type": "boolean",
                    "description": "boolean describing whether the user provided the item code or item name. True if the user provided the name, false if teh user provided the code."
                    },
                    "unit": {
                    "type": "string",
                    "description": "The number of items to check for - defaults to 1"
                    }
                },
                "required": ["item", "need_item_code"]
                }
            }},
            { "type": "function",
             "function": {
                 "name": "get_hours_util",
                "description": "Get the hours of a store",
                "parameters": {
                "type": "object",
                "properties": {
                    "store_id": {
                    "type": "string",
                    "description": "The store id of the store"
                    }
                },
                "required": ["store_id"]
                }
            }},
            { "type": "function",
             "function": {
                 "name": "get_image_util",
                "description": "Get an image of an item",
                "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                    "type": "string",
                    "description": "The item"
                    },
                    "need_item_code": {
                    "type": "boolean",
                    "description": "boolean describing whether the user provided the item code or item name. True if the user provided the name, false if teh user provided the code."
                    }
                },
                "required": ["item", "need_item_code"]
                }
            }},
            { "type": "function",
             "function": {
                 "name": "use_part_util",
                "description": "Use a part",
                "parameters": {
                "type": "object",
                "properties": {
                    "item_code": {
                    "type": "string",
                    "description": "The item"
                    },
                    "need_item_code": {
                    "type": "boolean",
                    "description": "boolean describing whether the user provided the item code or item name. True if the user provided the name, false if teh user provided the code."
                    }
                },
                "required": ["item", "need_item_code"]
                }
            }}
        ]
    )

    # Check if the response contains choices and is not empty
    if not response.choices:
        return("Error: No response from the model")
    
    image_url = None

    # If the response has tool calls, handle them
    if response.choices[0].message.tool_calls:

        func = handle_function_calls(response, user_input)
        response = func[0]
        image_url = func[1]

    # If the response has no tool calls, return the response
    else:
        response = response.choices[0].message.content

    return (response, image_url)


# Handle function calls for a response
def handle_function_calls(response, user_input):
    # For each tool call, get the function name and arguments
    out = ""
    image_url = None

    name = response.choices[0].message.tool_calls[0].function.name
    arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    # Get availability of a part
    if name == "get_availability_util":
        if "unit" in arguments:
            out += get_availability_util(arguments["item"], arguments["need_item_code"], arguments["unit"])
        else:
            out += get_availability_util(arguments["item"], arguments["need_item_code"])

    # Get pricing of a part
    elif name == "get_pricing_util":
        if "unit" in arguments:
            out += get_pricing_util(arguments["item"], arguments["need_item_code"], arguments["unit"])
        else:
            out += get_pricing_util(arguments["item"], arguments["need_item_code"])

    # Get hours
    elif name == "get_hours_util":
        out += get_hours_util(arguments["store_id"])

    # Get image
    elif name == "get_image_util":
        output = get_image_util(arguments["item"], arguments["need_item_code"])
        out += output[0]
        image_url = output[1]

    # Get info on how to use part
    elif name == "use_part_util":
        out += use_part_util(arguments["item"], user_input, arguments["need_item_code"])

    else:
        print("Error: Function not found")

    return (out, image_url)

# EXAMPLE
# print(make_chat_request("What is the availability of item LZA406103A?"))