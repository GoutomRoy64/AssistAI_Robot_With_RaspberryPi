
from .Tts_Player import play_tts, wait_until_finished

class LanguageManager:
    def __init__(self):
        self.current_lang = "en"
        self.lang_commands = {
            "en": ["change to bangla", "switch to bangla"],
            "bn": ["ইংরেজিতে পরিবর্তন", "ইংরেজিতে স্যুইচ"]
        }
    
    def set_language(self, lang):
        self.current_lang = lang
        msg = "ভাষা বাংলা তে পরিবর্তন করা হয়েছে" if lang == "bn" else "Language changed to English"
        play_tts(msg, lang)
        wait_until_finished()

    def check_language_change(self, text):
        text_lower = text.lower()
        if any(cmd in text_lower for cmd in self.lang_commands["en"]):
            self.set_language("bn")
            return True
        elif any(cmd in text_lower for cmd in self.lang_commands["bn"]):
            self.set_language("en")
            return True
        return False