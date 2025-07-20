from config import Config
from llm.chat_engine import query_llm
from voice.stt import STTManager
from voice.tts import TextToSpeech
from audio.playback import AudioPlayer
from audio.live_recorder import stream_audio_to_file

print("Mesmer booting... validating config...")
Config.validate_config()
print(" Config validated.")


stt_mgr = STTManager()
tts = TextToSpeech()
player = AudioPlayer()

if not stt_mgr.initialize():
    print(" STT initialization failed.")
    exit(1)


conversation_history = [
    {"role": "system", "content": "You are Mesmer, a helpful and friendly AI. Keep responses natural and concise."}
]


current_mode = Config.DEFAULT_MODE or "homie"

print(" Leopard STT engine initialized")
print(" Mesmer is ready! Say 'exit' to quit.\n")

while True:
    user_input = input(" Press Enter to start listening (or type 'exit' to quit): ").strip()
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("👋 Ending conversation. Bye!")
        break

    print("Capturing live input...")
    audio_path = stream_audio_to_file(silence_threshold=0.005, max_silence=4.0)  

    print(f" Transcribing with metadata: {audio_path}")
    user_text = stt_mgr.process_audio(audio_path)

    if not user_text:
        print(" No speech detected or transcription failed.")
        continue

    
    if user_text.lower().strip() in ["exit", "quit", "stop"]:
        print("👋 Ending conversation. Bye!")
        break

    
    if "therapist mode" in user_text.lower():
        current_mode = "therapist"
        print(" Switched to Therapist Mode")
        continue
    elif "homie mode" in user_text.lower() or "friend mode" in user_text.lower():
        current_mode = "homie"
        print(" Switched to Homie Mode")
        continue
    elif "funny mode" in user_text.lower():
        current_mode = "funny"
        print(" Switched to Funny Mode")
        continue

    # uSer text to conversation history
    conversation_history.append({"role": "user", "content": user_text})
    print(f" You said: {user_text}")

    #  qyery LLM with FULL history
    print(f"Prompt to LLM ({current_mode}): {user_text}")
    print(" Mesmer is thinking...")
    reply = query_llm(conversation_history, current_mode)

    #  qurery fails, continue gracefully
    if not reply:
        print(" LLM returned empty response.")
        continue

    print(f" Mesmer replied: {reply}")

    #append assistant reply to memory
    conversation_history.append({"role": "assistant", "content": reply})

    # conVert to speech with dynamic voice
    print("Converting to voice...")
    voice_id = Config.get_voice_id(current_mode)
    print(f"Using voice for {current_mode}: {voice_id}")
    audio_bytes = tts.synthesize_speech(reply, voice_id=voice_id)

    if audio_bytes:
        print("Playing back directly...")
        player.play_audio_bytes(audio_bytes)
    else:
        print("TTS synthesis failed.")