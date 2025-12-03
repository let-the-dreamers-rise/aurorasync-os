"""
Voice Engine for AuroraSync OS.
Conversational AI system for customer engagement via voice.
"""

from app.voice_engine.voice_agent import VoiceAgent
from app.voice_engine.tts_provider import TTSProvider, generate_tts
from app.voice_engine.stt_provider import STTProvider, transcribe_audio
from app.voice_engine.flow_manager import FlowManager
from app.voice_engine.message_templates import MessageTemplates
from app.voice_engine.conversation_scenarios import ConversationScenarios

__all__ = [
    "VoiceAgent",
    "TTSProvider",
    "generate_tts",
    "STTProvider",
    "transcribe_audio",
    "FlowManager",
    "MessageTemplates",
    "ConversationScenarios",
]
