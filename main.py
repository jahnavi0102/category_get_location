from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
from mapbox import get_category, get_locations

# Load your OpenAI API key
OpenAI.api_key = "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"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = "You are chatting with an AI. You are here to help with location search for different categories."


@bot()
def on_message(message_history: List[Message], state: dict = None):
    """
    Get proper locations with pin address for categories (even the smallest one.)
    """
    
    user_message = message_history[-1]['content']
    user_message = user_message[0]["value"]

    if len(message_history) == 1:
        bot_response_now = SYSTEM_PROMPT

    # Define available categories 
    categories = get_category()

    # Check user's message
    if "location" in user_message:
        bot_response_now = f'please select one: ({categories})'

    elif user_message.lower() in categories:
        selected_category = user_message.lower()
        bot_response_now = get_locations(category=selected_category)
    else:
        # Default response if no match
        bot_response_now = f"You can help  with category search. Please specify one of the available categories ({categories})."

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
            system_prompt=bot_response_now,
            message_history=message_history+[{"role": "assistant", "content": [{'data_type': 'STRING', 'value': bot_response_now}]}], 
            model="gpt-3.5-turbo",
        )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return  {
        "status_code": 200,
        "response": response
    }