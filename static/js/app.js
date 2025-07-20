// Blob Interface Controller
const micBlob = document.getElementById("micBlob");
const modeSwitch = document.getElementById("modeSwitch");
const modeLabel = document.getElementById("modeLabel");
const chatBox = document.getElementById("chatBox");
const sendBtn = document.getElementById("sendBtn");
const textInput = document.getElementById("textInput");

let isRecording = false;
let mediaRecorder;
let audioChunks = [];

// Blob click handler for recording
micBlob.addEventListener("click", async () => {
  if (!isRecording) {
    await startRecording();
  } else {
    stopRecording();
  }
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    audioChunks = [];

    mediaRecorder.ondataavailable = e => {
      if (e.data.size > 0) audioChunks.push(e.data);
    };

    mediaRecorder.onstop = sendAudioToBackend;
    mediaRecorder.start();
    
    isRecording = true;
    micBlob.classList.add('recording');
    
    // Update blob text
    document.querySelector('.blob-text').textContent = "Listening...";
    
  } catch (error) {
    console.error('Error accessing microphone:', error);
    alert('Could not access microphone. Please check permissions.');
  }
}

function stopRecording() {
  if (mediaRecorder) {
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
  }
  
  isRecording = false;
  micBlob.classList.remove('recording');
  micBlob.classList.add('processing');
  
  // Update blob text
  document.querySelector('.blob-text').textContent = "Processing...";
}

async function sendAudioToBackend() {
  const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
  const formData = new FormData();
  formData.append("audio", audioBlob, "input.webm");

  try {
    const response = await fetch("/process_audio", { method: "POST", body: formData });
    const data = await response.json();

    // Remove processing state
    micBlob.classList.remove('processing');
    document.querySelector('.blob-text').textContent = "Say hi to Mesmer";

    if (data.error) {
      alert(data.error);
      return;
    }

    // Handle mode switching
    if (data.mode) {
      if (data.mode === "therapist") {
        modeSwitch.checked = true;
        document.body.className = "therapist";
        modeLabel.textContent = "Therapist Mode";
      } else {
        modeSwitch.checked = false;
        document.body.className = "";
        modeLabel.textContent = "Homie Mode";
      }
      
      // Show mode switch message
      chatBox.innerHTML += `<p><strong>System:</strong> ${data.message}</p>`;
      return;
    }

    // Add conversation to chat
    chatBox.innerHTML += `<p><strong>You:</strong> ${data.transcript}</p>`;
    chatBox.innerHTML += `<p><strong>Mesmer:</strong> ${data.reply}</p>`;

    // Auto-scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Play audio response
    if (data.audio) {
      const binary = atob(data.audio);
      const arrayBuffer = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        arrayBuffer[i] = binary.charCodeAt(i);
      }

      const audioBlob = new Blob([arrayBuffer], { type: "audio/mpeg" });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    } else {
      console.warn("No audio returned from backend");
    }

  } catch (error) {
    console.error('Error sending audio:', error);
    micBlob.classList.remove('processing');
    document.querySelector('.blob-text').textContent = "Say hi to Mesmer";
    alert('Error processing audio. Please try again.');
  }
}

// Mode toggle handler
modeSwitch.addEventListener("change", async () => {
  const mode = modeSwitch.checked ? "therapist" : "homie";
  document.body.className = mode;
  modeLabel.textContent = mode === "therapist" ? "Therapist Mode" : "Homie Mode";

  try {
    await fetch("/switch_mode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode })
    });
  } catch (error) {
    console.error('Error switching mode:', error);
  }
});

// Text input handler
sendBtn.addEventListener("click", sendTextMessage);

textInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendTextMessage();
  }
});

async function sendTextMessage() {
  const userText = textInput.value.trim();
  if (!userText) return;

  // Add user message to chat
  chatBox.innerHTML += `<p><strong>You:</strong> ${userText}</p>`;
  textInput.value = "";

  // Auto-scroll to bottom
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/process_text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: userText })
    });

    const data = await response.json();
    
    if (data.error) {
      chatBox.innerHTML += `<p><strong>Error:</strong> ${data.error}</p>`;
      return;
    }

    // Add Mesmer's response
    chatBox.innerHTML += `<p><strong>Mesmer:</strong> ${data.reply}</p>`;

    // Auto-scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Play audio response
    if (data.audio) {
      const audioBlob = new Blob([Uint8Array.from(atob(data.audio), c => c.charCodeAt(0))], { type: "audio/mpeg" });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    }

  } catch (error) {
    console.error('Error sending text:', error);
    chatBox.innerHTML += `<p><strong>Error:</strong> Failed to send message</p>`;
  }
}

// Initialize interface
document.addEventListener('DOMContentLoaded', () => {
  // Set initial mode based on body class or default
  const initialMode = document.body.className || "homie";
  modeSwitch.checked = initialMode === "therapist";
  modeLabel.textContent = initialMode === "therapist" ? "Therapist Mode" : "Homie Mode";
});