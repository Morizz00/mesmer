import pvporcupine
import sounddevice as sd
import numpy as np
from config import Config

def listen_for_hotword():
    try:
        porcupine = pvporcupine.create(
            access_key=Config.PICOVOICE_ACCESS_KEY,
            keyword_paths=[pvporcupine.KEYWORD_PATHS['hey_mesmer']],  
            sensitivities=[Config.SENSITIVITY]
        )

        print(" Waiting for hotword...")

        def audio_callback(indata, frames, time, status):
            pcm = np.frombuffer(indata, dtype=np.int16)
            result = porcupine.process(pcm)
            if result >= 0:
                raise StopIteration  

        with sd.InputStream(
            channels=1,
            samplerate=porcupine.sample_rate,
            blocksize=porcupine.frame_length,
            dtype='int16',
            callback=audio_callback
        ):
            try:
                while True:
                    sd.sleep(100)  # just keepin this loop runnin
            except StopIteration:
                print(" Hotword detected!")
                return True

    except Exception as e:
        print(f"Error in hotword detection: {e}")
        return False
    finally:
        if porcupine:
            porcupine.delete()
