import pyttsx3
import os

engine = pyttsx3.init()
engine.setProperty('volume', 1.0)  # Max volume

# List available voices
voices = engine.getProperty('voices')
print("Available voices:")
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name} ({voice.languages})")

# Set a specific voice (e.g., index 0)
engine.setProperty('voice', voices[0].id)

# Adjust speed (200 is normal; lower for slower speech)
engine.setProperty('rate', 120)  # Slower speech for clarity

text = "Hello, this is a test of the AI voice companion for neurodiverse individuals."
output_path = os.path.join("output", "pyttsx3_output.wav")
os.makedirs("output", exist_ok=True)

engine.save_to_file(text, output_path)
engine.runAndWait()
print(f"TTS output saved as {output_path}")