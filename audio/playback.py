from io import BytesIO
import wave
import simpleaudio as sa
import threading
import playsound
import os

class AudioPlayer:
    def play_audio_bytes(self, audio_bytes: BytesIO):
        try:
            # Load wave from BytesIO properly
            with wave.open(audio_bytes, 'rb') as wav_file:
                wave_obj = sa.WaveObject.from_wave_read(wav_file)
                play_obj = wave_obj.play()
                play_obj.wait_done()
        except Exception as e:
            print(f"Error playing audio bytes: {e}")

    def play_audio_file(self, file_path: str):
        if not os.path.exists(file_path):
            print(f" FNf: {file_path}")
            return

        def _play():
            try:
                playsound.playsound(file_path)
            except Exception as e:
                print(f"Err in playback thread: {e}")

        threading.Thread(target=_play).start()

    def wait_for_completion(self):
        if hasattr(self, "thread"):
            self.thread.join()