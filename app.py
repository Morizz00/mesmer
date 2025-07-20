from flask import Flask, render_template, request, jsonify
import os
import base64
import subprocess
from config import Config
from llm.chat_engine import query_llm  
from voice.stt import STTManager
from voice.tts import TextToSpeech
from audio.playback import AudioPlayer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.AUDIO_TEMP_DIR


stt_mgr = STTManager()
tts = TextToSpeech()
player = AudioPlayer()

if not stt_mgr.initialize():
    print(" STT engine not initialized")
else:
    print(" STT engine initialized")


conversation_history = []
current_mode = Config.DEFAULT_MODE or "homie"

def get_system_prompt(mode):
    if mode == "therapist":
        return (
            "You are Mesmer, an empathetic therapist-like AI. "
            "Provide emotional support, validate feelings, and use calming language. "
            "Avoid dismissing the user. If severe distress is detected, suggest reaching out to a professional."
        )
    else:
        return (
            "You are Mesmer, a witty, supportive best friend with a pop-culture twist. "
            "Keep it fun, smart, and relatable—like someone who can roast you with love but always has your back."
        )

@app.route('/')
def index():
    return render_template('index.html', mode=current_mode)

@app.route('/switch_mode', methods=['POST'])
def switch_mode():
    global current_mode, conversation_history
    data = request.json
    new_mode = data.get('mode', 'homie')
    if new_mode in ["homie", "therapist"]:
        current_mode = new_mode
        conversation_history = []
        return jsonify({"status": "success", "mode": current_mode})
    return jsonify({"status": "error", "message": "Invalid mode"}), 400

@app.route('/process_audio', methods=['POST'])
def process_audio():
    global conversation_history, current_mode

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    os.makedirs(Config.AUDIO_TEMP_DIR, exist_ok=True)

    original_path = os.path.join(Config.AUDIO_TEMP_DIR, "input.webm")
    audio_file.save(original_path)

    wav_path = os.path.join(Config.AUDIO_TEMP_DIR, "input.wav")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", original_path,
            "-ac", "1", "-ar", "16000", wav_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except Exception as e:
        print(f" FFmpeg conversion failed: {e}")
        return jsonify({"error": "Audio conversion failed"}), 500

    user_text = stt_mgr.process_audio(wav_path)

    for path in [original_path, wav_path]:
        if os.path.exists(path):
            os.remove(path)

    if not user_text:
        return jsonify({"error": "Transcription failed"}), 500

    if "therapist mode" in user_text.lower():
        current_mode = "therapist"
        conversation_history = []
        return jsonify({"mode": "therapist", "message": "Mode switched to Therapist"}), 200
    elif "homie mode" in user_text.lower():
        current_mode = "homie"
        conversation_history = []
        return jsonify({"mode": "homie", "message": "Mode switched to Homie"}), 200

    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, {"role": "system", "content": get_system_prompt(current_mode)})

    conversation_history.append({"role": "user", "content": user_text})
    print(f"You said: {user_text} ({current_mode})")

    reply = query_llm(conversation_history, current_mode)
    if not reply:
        reply = "Hmm, I couldn't process that, but I'm here for you!"

    conversation_history.append({"role": "assistant", "content": reply})

    voice_id = Config.get_voice_id(current_mode)
    audio_bytes = tts.synthesize_speech(reply, voice_id=voice_id)

    response = {"transcript": user_text, "reply": reply}
    if audio_bytes:
        response["audio"] = base64.b64encode(audio_bytes.getvalue()).decode('utf-8')

    return jsonify(response), 200

@app.route('/process_text', methods=['POST'])
def process_text():
    global conversation_history, current_mode

    data = request.json
    user_text = data.get("text")
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, {"role": "system", "content": get_system_prompt(current_mode)})

    conversation_history.append({"role": "user", "content": user_text})
    print(f"User ({current_mode}): {user_text}")

    reply = query_llm(conversation_history, current_mode)
    if not reply:
        reply = "Hmm, I couldn't process that, but I'm here for you!"

    conversation_history.append({"role": "assistant", "content": reply})
    print(f"Mesmer ({current_mode}): {reply}")

    voice_id = Config.get_voice_id(current_mode)
    audio_bytes = tts.synthesize_speech(reply, voice_id=voice_id)

    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode('utf-8') if audio_bytes else None
    return jsonify({"reply": reply, "audio": audio_base64}), 200

if __name__ == '__main__':
    app.run(debug=True)