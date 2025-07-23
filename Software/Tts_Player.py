import pygame
from gtts import gTTS
from io import BytesIO
import os
from .Servo import send_to_arduino
import time
# Import is now at the top level for better practice and to avoid circular dependencies.
from .Face_Display import set_face_state

pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

def play_tts(text, lang='en'):
    """
    Generates and plays TTS audio. Sets face state to 'talking' immediately.
    """
    if not text:
        print("TTS Error: Received empty text.")
        return

    # Set the face to 'talking' as soon as we decide to speak.
    set_face_state('talking')

    fp = None
    retries = 3
    for attempt in range(retries):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            print("[TTS] Successfully generated audio online.")
            break
        except Exception as e:
            print(f"[TTS Warning] Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(0.5)
            else:
                print("[TTS Error] Online TTS failed after multiple retries.")
                fp = None

    try:
        if fp:
            pygame.mixer.music.stop()
            send_to_arduino("talk")
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            time.sleep(0.1)
        else:
            print("[TTS] Falling back to offline 'espeak' synthesizer.")
            os.system(f'espeak -v {lang} "{text}"')
            send_to_arduino("rest")
            
    except Exception as e:
        print(f"TTS Playback Error: {e}")
        send_to_arduino("rest")

def stop_tts():
    pygame.mixer.music.stop()
    send_to_arduino("rest")
    set_face_state('idle')

def is_playing():
    return pygame.mixer.music.get_busy()

def wait_until_finished():
    """
    A simple blocking function to wait for audio to finish.
    It no longer changes the face state.
    """
    while is_playing():
        time.sleep(0.1)
