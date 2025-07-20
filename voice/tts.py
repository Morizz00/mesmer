from pydub import AudioSegment
from io import BytesIO
import requests
from config import Config

class TextToSpeech:
    def __init__(self):
        self.api_key = Config.ELEVENLABS_API_KEY
        self.model_id = Config.ELEVENLABS_MODEL

    def synthesize_speech(self, text: str, voice_id: str = None) -> BytesIO:
        if not voice_id:
            voice_id = Config.get_voice_id("homie")  # dihfault to homie mode voice

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.6,           
                "similarity_boost": 0.7     
            }
        }

        try:
            print(f" Sending text to ElevenLabs using voice: {voice_id}")
            response = requests.post(url, headers=headers, json=payload, stream=True)
            response.raise_for_status()

            mp3_audio = BytesIO(response.content)
            audio = AudioSegment.from_file(mp3_audio, format="mp3")

            wav_buffer = BytesIO()
            audio.export(wav_buffer, format="wav")
            wav_buffer.seek(0)

            return wav_buffer

        except requests.exceptions.RequestException as e:
            print(f"ElevenLabs TTS request error: {e}")
        except Exception as e:
            print(f"ElevenLabs TTS processing error: {e}")

        return None