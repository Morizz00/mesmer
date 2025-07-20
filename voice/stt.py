import pvleopard
import os
import time
from typing import Optional
from config import Config


class SpeechToText:
    def __init__(self):
        self.leopard = None
        self._initialize_leopard()

    def _initialize_leopard(self):
        try:
            self.leopard = pvleopard.create(
                access_key=Config.PICOVOICE_ACCESS_KEY
            )
            print("Leopard STT engine initialized")
        except Exception as e:
            print(f"Error initializing Leopard STT: {e}")
            raise

    def transcribe_file(self, audio_file: str) -> Optional[str]:
        """Transcribe audio file to text"""
        if not os.path.exists(audio_file):
            print(f"Audio file not found: {audio_file}")
            return None

        try:
            print(f"Transcribing audio: {audio_file}")
            start_time = time.time()
            transcript, words = self.leopard.process_file(audio_file)
            processing_time = time.time() - start_time

            if transcript and transcript.strip():
                print(f"Transcription completed in {processing_time:.2f}s")
                print(f"Transcript: '{transcript}'")
                return transcript.strip()
            else:
                print(" No speech detected in audio file")
                return None
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None

    def transcribe_with_metadata(self, audio_file: str) -> Optional[dict]:
        """Transcribe audio file and return detailed metadata"""
        if not os.path.exists(audio_file):
            print(f"Audio file not found: {audio_file}")
            return None

        try:
            print(f" Transcribing with metadata: {audio_file}")
            start_time = time.time()
            transcript, words = self.leopard.process_file(audio_file)
            processing_time = time.time() - start_time

            if transcript and transcript.strip():
                avg_confidence = sum(word.confidence for word in words) / len(words) if words else 0.0
                return {
                    'transcript': transcript.strip(),
                    'words': words,
                    'word_count': len(words),
                    'processing_time': processing_time,
                    'average_confidence': avg_confidence,
                    'file_path': audio_file
                }
            else:
                print("No speech detected in audio file")
                return None
        except Exception as e:
            print(f"Error transcribing audio with metadata: {e}")
            return None

    def cleanup(self):
        if self.leopard:
            self.leopard.delete()

    def __del__(self):
        self.cleanup()


class STTManager:
    
    def __init__(self):
        self.stt = None
        self.last_transcript = None
        self.last_confidence = 0.0
        self.initialized = False

    def initialize(self) -> bool:
        
        try:
            self.stt = SpeechToText()
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize STT manager: {e}")
            self.initialized = False
            return False

    def process_audio(self, audio_file: str) -> Optional[str]:
        if not self.initialized or not self.stt:
            print("STT engine not initialized")
            return None

        try:
            result = self.stt.transcribe_with_metadata(audio_file)
            if result:
                self.last_transcript = result['transcript']
                self.last_confidence = result['average_confidence']
                # cLeanin up audio filez
                try:
                    os.remove(audio_file)
                    print(f"Cleaned up audio file: {audio_file}")
                except:
                    pass
                return self.last_transcript
            else:
                print("no speech detected or transcription failed")
                return None
        except Exception as e:
            print(f"eror processing audio: {e}")
            return None

    def get_last_confidence(self) -> float:
        return self.last_confidence

    def cleanup(self):
        if self.stt:
            self.stt.cleanup()