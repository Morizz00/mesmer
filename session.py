from typing import Dict, Optional
from models import Conversation
import uuid

class SessionManager:
    def __init__(self):
        # In-memory storage for sessions (use a database for persistence)
        self.sessions: Dict[str, list[Conversation]] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        return session_id

    def add_to_session(self, session_id: str, user_input: str, ai_response: str, speed: float, voice_index: int, stt_status: str = "success") -> None:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} does not exist")
        conversation = Conversation(
            user_input=user_input,
            ai_response=ai_response,
            speed=speed,
            voice_index=voice_index,
            session_id=session_id,
            stt_status=stt_status
        )
        self.sessions[session_id].append(conversation)

    def get_session_history(self, session_id: str) -> list[Conversation]:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} does not exist")
        return self.sessions[session_id]

session_manager = SessionManager()