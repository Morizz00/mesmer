import sounddevice as sd
import soundfile as sf
import os
import time
from config import Config

def record_audio(output_file: str = "temp_audio/user_input.wav", duration: int = Config.RECORD_TIMEOUT):
    """Record audio from microphone and save as WAV"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    samplerate = Config.SAMPLE_RATE
    channels = Config.CHANNELS

    print(f"🎙️ Recording for {duration} seconds...")

    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
        sd.wait()  # Wait until recording is finished
        sf.write(output_file, recording, samplerate)
        print(f" Audio saved to {output_file}")
        return output_file
    except Exception as e:
        print(f" Error during recording: {e}")
        return None
