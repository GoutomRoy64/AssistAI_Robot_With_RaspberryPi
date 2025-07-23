#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

# --- Local Imports ---
from Software.Face_Recognition import FaceRecognizer 
from Software.Tts_Player import play_tts, wait_until_finished
from Software.Speech_Listener import SpeechListener
from Software.Language_Manager import LanguageManager
from Software.Response_Generator import generate_response
from Software.Tts_Player import play_tts, stop_tts, is_playing
from Software.Face_Display import init_display, set_face_state, shutdown_display, update_display

def main():
    print("AssistAI is starting...")
    
    # --- Face Recognition Setup ---
    # 2. Create an instance of the recognizer
    face_recognizer = FaceRecognizer()
    
    # 3. Load the model. If it fails, it probably needs training.
    if not face_recognizer.load_trained_model():
        print("Attempting to train a new model...")
        if not face_recognizer.train():
            print("FATAL: Model training failed. Exiting.")
            return # Exit if training fails
        # Try loading again after training
        face_recognizer.load_trained_model()

    # 4. Recognize the user
    # This will now run for up to 10 seconds and require 5 confident matches
    user_name = face_recognizer.recognize_face()

    if not user_name:
        user_name = "Unknown" # Assign a default name if no one is recognized

    # --- The rest of your main function ---
    if user_name == "Unknown":
        play_tts("I don't recognize you, but I will assist you anyway.", "en")
        wait_until_finished()
    else:
        # Capitalize the first letter for a nicer greeting
        play_tts(f"Hello, {user_name.capitalize()}. I am ready.", "en")
        wait_until_finished()
    
    init_display()
    

    
    lang_manager = LanguageManager()
    speech_listener = SpeechListener()
    
    # --- Program States ---
    robot_state = 'IDLE'

    # --- Initial Greeting ---
    play_tts(f"হ্যালো {user_name}! আমি প্রস্তুত।", "bn")
    while is_playing():
        update_display()
        time.sleep(0.05)
    
    # --- Keyword Definitions ---
    exit_phrases = {
        "en": ["exit", "stop program", "quit", "goodbye"],
        "bn": ["বন্ধ", "বিদায়", "চলে যাও"]
    }
    interrupt_words = {
        "en": ["stop", "enough", "shut up", "cancel"],
        "bn": ["থামো", "থাম", "চুপ কর"]
    }

    # --- Main Interaction Loop ---
    while True:
        update_display()

        if robot_state == 'IDLE':
            set_face_state('idle')
            speech_listener.start_listening("bn-BD" if lang_manager.current_lang == "bn" else "en-US")
            robot_state = 'LISTENING'

        elif robot_state == 'LISTENING':
            user_input = speech_listener.get_transcribed_text()
            
            if user_input is not None:
                robot_state = 'PROCESSING' if user_input else 'IDLE'
        
        elif robot_state == 'PROCESSING':
            set_face_state('thinking')
            
            if lang_manager.check_language_change(user_input):
                robot_state = 'IDLE'
                continue

            if any(phrase in user_input.lower() for phrase in exit_phrases[lang_manager.current_lang]):
                bye_msg = "বিদায়! ভালো থাকবেন" if lang_manager.current_lang == "bn" else "Goodbye! Stay well"
                play_tts(bye_msg, lang_manager.current_lang)
                while is_playing(): update_display(); time.sleep(0.05)
                break

            response = generate_response(user_input, user_name, lang_manager.current_lang)
            play_tts(response, lang_manager.current_lang)
            robot_state = 'SPEAKING'

        elif robot_state == 'SPEAKING':
            # Start the interrupt listener. It will run continuously in the background.
            lang_code = "bn-BD" if lang_manager.current_lang == "bn" else "en-US"
            stop_words = interrupt_words[lang_manager.current_lang]
            speech_listener.start_interrupt_listener(lang_code, stop_words)

            # Loop as long as the robot is talking
            while is_playing():
                update_display()
                if speech_listener.interrupt_event.is_set():
                    print("Interrupt command received. Stopping speech.")
                    stop_tts()
                    break
                time.sleep(0.05)
            
            # CRUCIAL: Stop the interrupt listener thread to free up the microphone.
            speech_listener.stop_interrupt_listener()
            robot_state = 'IDLE'

        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\nProgram interrupted by user. Shutting down.")
    finally:
        shutdown_display()
        print("AssistAI has shut down.")
