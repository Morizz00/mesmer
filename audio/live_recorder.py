import sounddevice as sd
import numpy as np
import queue
import wave
import os
import time
from config import Config


q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print(f" Audio Stream Status: {status}")
    q.put(indata.copy())

def stream_audio_to_file(
    output_path="temp_audio/live_input.wav",
    silence_threshold=0.005,  
    max_silence=4.0,          
    max_duration=100          
):
    """
    Streams audio from the microphone until silence is detected or max_duration reached.
    Saves the result as a WAV file and returns the file path.
    """
    samplerate = Config.SAMPLE_RATE
    channels = Config.CHANNELS
    chunk_duration = Config.CHUNK_SIZE / samplerate
    silence_limit_chunks = int(max_silence / chunk_duration)

    print(" Listening for your speech..")
    frames = []
    silence_chunks = 0
    start_time = time.time()

    with sd.InputStream(samplerate=samplerate, channels=channels, callback=audio_callback):
        while True:
            try:
                data = q.get(timeout=1)
            except queue.Empty:
                continue

            frames.append(data)
            rms = np.sqrt(np.mean(data ** 2)) 
            print(f"🎚️ RMS: {rms:.4f}", end="\r")

      
            if rms < silence_threshold:
                silence_chunks += 1
            else:
                silence_chunks = 0

            if silence_chunks > silence_limit_chunks:
                print("\n Silence detected. Stopping.")
                break

            if time.time() - start_time > max_duration:
                print("\n Max duration reached. Stopping.")
                break

    
    audio_data = np.concatenate(frames, axis=0)
    audio_data = (audio_data * 32767).astype(np.int16)  
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    duration = round(time.time() - start_time, 2)
    print(f" Audio saved to {output_path} | Duration: {duration}s")

    return output_path