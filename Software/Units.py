import pygame
import time
import re
from .Servo import send_to_arduino

def play_sound(file_path):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        send_to_arduino("talk")
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)
        send_to_arduino("rest")
        time.sleep(0.1)
    except Exception as e:
        print(f"Sound playback error: {e}")

def clean_response(text):
    """
    Cleans text from the AI by removing common Markdown and unwanted characters.
    """
    if not text:
        return ""
    # Remove Markdown characters like *, #, `
    text = re.sub(r'[\*#`]', '', text)
    # Remove any standalone quotes
    text = text.replace('"', '')
    # Strip leading/trailing whitespace
    return text.strip()

def translate_text(text, dest='bn'):
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='auto', target=dest).translate(text)
    except ImportError:
        from googletrans import Translator
        return Translator().translate(text, dest=dest).text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
