import ctypes
import os

# Absolute path to the DLL
dll_path = os.path.abspath("target/release/audio_capture.dll")
print(f"Loading DLL from: {dll_path}")  # Optional debug print

lib = ctypes.CDLL(dll_path)

lib.clean_audio.argtypes = [ctypes.c_char_p]
lib.clean_audio.restype = ctypes.c_char_p

def clean_audio(path: str) -> str:
    result = lib.clean_audio(path.encode())
    return result.decode()

# Test
print(clean_audio("temp_audio/user_input.wav"))