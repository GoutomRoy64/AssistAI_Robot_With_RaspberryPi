from .AI_Handler import gemini_api
from .Units import clean_response, translate_text
import collections

# Use a deque to automatically manage the size of the conversation history
conversation_history = collections.deque(maxlen=4) # Stores last 4 turns (2 user, 2 AI)

def generate_response(input_text, user_name, current_lang):
    """
    Generates a response, maintaining and using conversation history.
    """
    global conversation_history
    
    input_lower = input_text.lower()
    
    # Handle hardcoded simple commands first
    if any(x in input_lower for x in ["your name", "তোমার নাম"]):
        return f"আমার নাম Assist AI, আর আপনি {user_name}।" if current_lang == "bn" else f"My name is Assist AI, and you're {user_name}."
    if any(x in input_lower for x in ["hello", "হ্যালো"]):
        return f"হ্যালো {user_name}! আমি আপনাকে কিভাবে সাহায্য করতে পারি?" if current_lang == "bn" else f"Hello {user_name}! How can I assist you today?"
    if any(x in input_lower for x in ["creator", "নির্মাতা"]):
        return "গৌতম রায়, আয়ুষ দাস, মাহমুদুল, এবং টোমা" if current_lang == "bn" else "Goutom Roy, Ayush Das, Mahamudul, and Toma"
    
    # Generate response using the AI with history
    history_list = list(conversation_history)
    english_response = gemini_api(input_text, history=history_list)
    
    # Add the current exchange to history
    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"AI: {english_response}")
    
    # Translate if necessary and return
    if current_lang == "bn":
        return translate_text(clean_response(english_response), 'bn')
    else:
        return clean_response(english_response)

