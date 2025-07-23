import speech_recognition as sr
import threading
import time
from queue import Queue
from .Units import play_sound
from .Face_Display import set_face_state

LISTEN_SOUND = "Resources/listen.mp3"
PROCESS_SOUND = "Resources/convert.mp3"

class SpeechListener:
    """
    A class to handle speech recognition in non-blocking background threads.
    Now includes a persistent interrupt listener for more robust command interruption.
    """
    def __init__(self):
        # Recognizer for main commands
        self.main_recognizer = sr.Recognizer()
        self.main_recognizer.dynamic_energy_threshold = True
        self.main_recognizer.pause_threshold = 0.8
        
        # A separate, more sensitive recognizer for interruptions
        self.interrupt_recognizer = sr.Recognizer()
        self.interrupt_recognizer.dynamic_energy_threshold = True
        self.interrupt_recognizer.pause_threshold = 0.5 # Quicker to react

        self.text_queue = Queue()
        self.is_listening = False
        
        # --- Thread control events ---
        self.interrupt_event = threading.Event() # Signals that a stop word was heard
        self.stop_interrupt_thread = threading.Event() # Signals the interrupt thread to stop completely
        self.interrupt_thread = None

    def _listen_thread(self, language):
        """The target function for the main listening thread."""
        self.is_listening = True
        with sr.Microphone() as source:
            try:
                self.main_recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio = self.main_recognizer.listen(source, timeout=5, phrase_time_limit=8)
                set_face_state('thinking')
                play_sound(PROCESS_SOUND)
                text = self.main_recognizer.recognize_google(audio, language=language)
                self.text_queue.put(text)
                print(f"You said: {text}")
            except Exception as e:
                print(f"Listen error: {e}")
                self.text_queue.put("")
            finally:
                self.is_listening = False

    def start_listening(self, language="bn-BD"):
        """Starts the main listening process."""
        if self.is_listening:
            return
        set_face_state('listening')
        play_sound(LISTEN_SOUND)
        while not self.text_queue.empty():
            self.text_queue.get()
        thread = threading.Thread(target=self._listen_thread, args=(language,), daemon=True)
        thread.start()

    def get_transcribed_text(self):
        """Checks the queue for transcribed text."""
        if not self.text_queue.empty():
            return self.text_queue.get()
        return None

    def _interrupt_loop(self, language, stop_words):
        """
        A continuous loop running in a thread, listening only for stop words.
        """
        print("[Interrupt Loop] Started.")
        with sr.Microphone() as source:
            self.interrupt_recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while not self.stop_interrupt_thread.is_set():
                try:
                    # Listen for a short phrase
                    audio = self.interrupt_recognizer.listen(source, timeout=1, phrase_time_limit=2)
                    text = self.interrupt_recognizer.recognize_google(audio, language=language)
                    print(f"[Interrupt Listener] Heard: {text}")
                    if any(word in text.lower() for word in stop_words):
                        print("[Interrupt Listener] Stop word detected!")
                        self.interrupt_event.set()
                        break # Exit loop once detected
                except sr.UnknownValueError:
                    # This is expected, just means no one spoke. Loop continues.
                    continue
                except Exception as e:
                    # Avoid spamming errors if microphone has issues
                    time.sleep(1)
        print("[Interrupt Loop] Stopped.")

    def start_interrupt_listener(self, language, stop_words):
        """Starts the continuous interrupt listening thread."""
        if self.interrupt_thread and self.interrupt_thread.is_alive():
            return # Listener is already running
        
        self.interrupt_event.clear()
        self.stop_interrupt_thread.clear()
        
        self.interrupt_thread = threading.Thread(
            target=self._interrupt_loop,
            args=(language, stop_words),
            daemon=True
        )
        self.interrupt_thread.start()

    def stop_interrupt_listener(self):
        """Signals the interrupt listening thread to stop."""
        if self.interrupt_thread and self.interrupt_thread.is_alive():
            self.stop_interrupt_thread.set()
            self.interrupt_thread.join(timeout=1.5) # Wait for thread to exit
        self.interrupt_event.clear()

