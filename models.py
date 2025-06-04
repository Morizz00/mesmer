from pydantic import BaseModel
from typing import Optional

class Conversation(BaseModel):
    user_input: str
    ai_response: str
    voice_index: int = 0
    speed: float = 1.0
    session_id: Optional[str] = None
    stt_status: str = "success"  # Add this to track STT outcome