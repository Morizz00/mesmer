import pyttsx3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', 1.0)
        self.voices = self.engine.getProperty('voices')
        self.current_voice_index = 0

    def synthesize(self, text: str, output_file: str = None, speed: float = 1.0, voice_index: int = 0) -> bytes:
        if not text:
            raise ValueError("Text input cannot be empty")
        if not (0 <= voice_index < len(self.voices)):
            raise ValueError(f"Voice index {voice_index} out of range. Available: 0-{len(self.voices)-1}")
        
        self.engine.setProperty('voice', self.voices[voice_index].id)
        self.current_voice_index = voice_index
        rate = int(200 * speed)
        self.engine.setProperty('rate', max(50, min(300, rate)))

        if output_file:
            output_path = os.path.join(OUTPUT_DIR, output_file)
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            print(f"TTS output saved as {output_path} with voice {self.voices[voice_index].name} at rate {rate}")
            with open(output_path, "rb") as f:
                return f.read()
        else:
            raise NotImplementedError("Direct byte output not supported; use output_file.")

    def get_available_voices(self):
        return {i: voice.name for i, voice in enumerate(self.voices)}

    def set_voice(self, voice_index: int):
        if not (0 <= voice_index < len(self.voices)):
            raise ValueError(f"Voice index {voice_index} out of range. Available: 0-{len(self.voices)-1}")
        self.current_voice_index = voice_index
        self.engine.setProperty('voice', self.voices[voice_index].id)

tts_service = TTSService()