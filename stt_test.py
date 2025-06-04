import speech_recognition as sr
import os

def speech_to_text(audio_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_sphinx(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {str(e)}"

if __name__ == "__main__":
    audio_path = "test.wav"
    text = speech_to_text(audio_path)
    print(f"Recognized text: {text}")