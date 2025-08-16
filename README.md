Mesmer: AI Voice Assistant

Mesmer is a next-gen conversational AI that acts as your homie or therapist — built with Flask, Fine-tuned LLM (Phi-2)   , Speech-to-Text, and Text-to-Speech. It provides voice interaction, mode switching, and runs locally on GPU for blazing-fast inference.


---

 Features

Fine-Tuned AI Model

Runs on Microsoft Phi-2, fine-tuned for friendly & therapeutic conversations.


Dual Personality Modes

homie → Gen-Z friendly homeboy with humor.

therapist → Empathetic, calm mental-health support tone.


Voice Support

STT: Converts speech to text using Picovoice Leopard.

TTS: Uses ElevenLabs API for realistic speech synthesis.


Local GPU Acceleration

Fully optimized for RTX 4050 (or any CUDA GPU).


Web Interface

Built with Flask + HTML/JS for easy interaction.


Offline LLM

No API dependency for text generation when running locally.




---

⚙ Tech Stack

Backend: Python, Flask

LLM: Microsoft Phi-2 (fine-tuned) via HuggingFace

Speech:

STT: Picovoice Leopard

TTS: ElevenLabs


Frontend: HTML, CSS, JavaScript

Hardware: NVIDIA RTX 4050 (GPU inference)

(Additional features are yet to be added using Golang and Rust right now its mostly unused)



---

 Project Structure

mesmer/
├── app.py                   # Flask server
├── config.py                # API keys & global settings
├── llm/
│   ├── chat_engine.py       # Handles LLM interaction
│   └── prompt_templates.py  # Pre-defined prompts
├── voice/
│   ├── stt.py               # Speech-to-text logic
│   ├── tts.py               # Text-to-speech logic
│   └── playback.py          # Audio playback
├── static/
│   ├── css/style.css        # UI styles
│   └── js/app.js            # Client-side logic
├── templates/
│   └── index.html           # Main UI
└── .env                     # Environment variables


---

 Environment Variables

Create a .env file in the root:

OPENROUTER_API_KEY=your_openrouter_key
ELEVENLABS_API_KEY=your_elevenlabs_key
PICOVOICE_ACCESS_KEY=your_picovoice_key
DEFAULT_MODE=homie


---

 Setup & Run

1. Clone Repo

git clone https://github.com/Morizz00/mesmer.git
cd mesmer

2. Install Requirements

pip install -r requirements.txt

3. Download or Train Model

Fine-tuned model should be in ./finetuned_mesmer

Or update model_path in llm/chat_engine.py


4. Run App

python app.py

Access the web UI:

http://127.0.0.1:5000


---

 GPU Acceleration

Ensure you have:

CUDA Toolkit installed

PyTorch with GPU support:


pip install torch --index-url https://download.pytorch.org/whl/cu121


---

 Future Roadmap

 Add Whisper for STT fallback

 Mobile-first UI redesign

 Memory persistence for long conversations

 Deploy on Docker



---

 License

MIT License. Free to use & modify.
