import speech_recognition as sr

class STTService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self, audio_path: str) -> str:
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_sphinx(audio)
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {str(e)}"

stt_service = STTService()