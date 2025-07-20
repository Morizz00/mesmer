import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    PICOVOICE_ACCESS_KEY = os.getenv('PICOVOICE_ACCESS_KEY', '')  

    # Voices
    ELEVENLABS_VOICES = {
        "homie": os.getenv('ELEVENLABS_VOICE_FRIENDLY', 'cNYrMw9glwJZXR8RwbuR'),
        "therapist": os.getenv('ELEVENLABS_VOICE_THERAPIST', 'ZT9u07TYPVl83ejeLakq')
    }
    ELEVENLABS_MODEL = os.getenv('ELEVENLABS_MODEL', 'eleven_monolingual_v1')

    # LLM Config
    SELECTED_LLM = os.getenv('SELECTED_LLM', 'local')  
    LOCAL_MODEL_PATH = os.getenv('LOCAL_MODEL_PATH', './finetuned_mesmer') 

    # Audio
    AUDIO_TEMP_DIR = os.getenv('AUDIO_TEMP_DIR', 'temp_audio')

    DEFAULT_MODE = os.getenv('DEFAULT_MODE', 'homie')

    FALLBACK_RESPONSES = [
        "I'm sorry, I'm having trouble connecting to my services right now.",
        "Let me try that again in a moment.",
        "I'm experiencing some technical difficulties. Please try again."
    ]

    @classmethod
    def get_voice_id(cls, mode):
        return cls.ELEVENLABS_VOICES.get(mode, cls.ELEVENLABS_VOICES["homie"])
