"""
Speech-to-Text (STT) Provider for AuroraSync OS.
Mock implementation for demo purposes.
"""

from typing import Dict, Any, Optional
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class STTProvider:
    """
    Speech-to-Text provider for transcribing audio.
    
    This is a mock implementation for demo purposes.
    In production, this would integrate with services like:
    - Google Cloud Speech-to-Text
    - Amazon Transcribe
    - Azure Speech Services
    - Whisper (OpenAI)
    - AssemblyAI
    """
    
    # Mock transcriptions for common responses
    MOCK_TRANSCRIPTIONS = {
        "yes": ["yes", "yeah", "sure", "okay", "ok", "definitely", "absolutely"],
        "no": ["no", "nope", "not now", "maybe later", "not interested"],
        "safety": ["is it safe to drive", "can I drive", "is it dangerous", "should I stop driving"],
        "cost": ["how much will it cost", "what's the price", "cost estimate", "how expensive"],
        "reschedule": ["can we reschedule", "different time", "another day", "not available"],
        "morning": ["morning works", "morning is good", "9 am", "10 am"],
        "afternoon": ["afternoon works", "afternoon is good", "2 pm", "3 pm"],
        "evening": ["evening works", "evening is good", "6 pm", "7 pm"],
        "satisfied": ["very satisfied", "satisfied", "happy with service", "good service"],
        "not_satisfied": ["not satisfied", "unhappy", "poor service", "disappointed"]
    }
    
    def __init__(self):
        """Initialize STT provider."""
        self.transcription_count = 0
        logger.info("STT Provider initialized with mock transcription")
    
    def transcribe_audio(
        self,
        audio_file: Any,
        language: str = "en-IN",
        model: str = "default"
    ) -> Dict[str, Any]:
        """
        Transcribe audio file to text.
        
        Args:
            audio_file: Audio file (in production, this would be actual audio data)
            language: Language code (default: en-IN for Indian English)
            model: Model to use for transcription
        
        Returns:
            Dictionary with transcription results:
                - text: Transcribed text
                - confidence: Confidence score (0.0 to 1.0)
                - language: Detected language
                - duration: Audio duration in seconds
                - words: Word-level timestamps (optional)
        """
        self.transcription_count += 1
        
        # For demo, return mock transcription based on count
        mock_responses = [
            "Yes, please book the appointment",
            "Is it safe to drive?",
            "How much will this cost?",
            "Can we reschedule for tomorrow?",
            "I'm very satisfied with the service",
            "No, not right now",
            "Morning works better for me",
            "What are my options?",
            "Okay, go ahead",
            "Tell me more about the issue"
        ]
        
        # Cycle through mock responses
        text = mock_responses[self.transcription_count % len(mock_responses)]
        
        # Simulate confidence score
        confidence = 0.85 + (self.transcription_count % 10) * 0.01
        
        # Simulate duration
        duration = len(text.split()) * 0.5  # ~0.5 seconds per word
        
        response = {
            "text": text,
            "confidence": round(confidence, 2),
            "language": language,
            "language_detected": language,
            "duration": round(duration, 2),
            "word_count": len(text.split()),
            "transcribed_at": datetime.utcnow().isoformat() + "Z",
            "model": model,
            "is_mock": True
        }
        
        logger.info(f"Transcribed audio #{self.transcription_count}: '{text}' (confidence: {confidence:.2f})")
        
        return response
    
    def transcribe_audio_stream(
        self,
        audio_stream: Any,
        language: str = "en-IN"
    ) -> Dict[str, Any]:
        """
        Transcribe streaming audio (real-time).
        
        Args:
            audio_stream: Audio stream
            language: Language code
        
        Returns:
            Transcription results
        """
        # For demo, just call regular transcription
        return self.transcribe_audio(audio_stream, language)
    
    def detect_intent(self, text: str) -> Dict[str, Any]:
        """
        Detect user intent from transcribed text.
        
        Args:
            text: Transcribed text
        
        Returns:
            Intent detection results
        """
        text_lower = text.lower()
        
        # Simple keyword-based intent detection
        intents = {
            "confirm": ["yes", "yeah", "sure", "okay", "ok", "definitely", "book"],
            "decline": ["no", "nope", "not now", "maybe later", "not interested"],
            "safety_inquiry": ["safe", "drive", "dangerous", "risk"],
            "cost_inquiry": ["cost", "price", "expensive", "how much"],
            "reschedule": ["reschedule", "different time", "another day", "change"],
            "time_preference": ["morning", "afternoon", "evening", "weekend"],
            "satisfaction": ["satisfied", "happy", "good", "excellent"],
            "dissatisfaction": ["not satisfied", "unhappy", "poor", "bad"]
        }
        
        detected_intent = "unknown"
        confidence = 0.5
        
        for intent, keywords in intents.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_intent = intent
                confidence = 0.85
                break
        
        return {
            "intent": detected_intent,
            "confidence": confidence,
            "text": text,
            "entities": self._extract_entities(text)
        }
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text (mock implementation)."""
        entities = {}
        
        text_lower = text.lower()
        
        # Extract time preferences
        if "morning" in text_lower:
            entities["time_preference"] = "morning"
        elif "afternoon" in text_lower:
            entities["time_preference"] = "afternoon"
        elif "evening" in text_lower:
            entities["time_preference"] = "evening"
        
        # Extract satisfaction level
        if any(word in text_lower for word in ["very satisfied", "excellent"]):
            entities["satisfaction_level"] = 5
        elif any(word in text_lower for word in ["satisfied", "good"]):
            entities["satisfaction_level"] = 4
        elif any(word in text_lower for word in ["okay", "fine"]):
            entities["satisfaction_level"] = 3
        
        return entities


# Global STT provider instance
_stt_provider = None


def get_stt_provider() -> STTProvider:
    """Get singleton STT provider instance."""
    global _stt_provider
    if _stt_provider is None:
        _stt_provider = STTProvider()
    return _stt_provider


def transcribe_audio(
    audio_file: Any,
    language: str = "en-IN",
    model: str = "default"
) -> Dict[str, Any]:
    """
    Convenience function to transcribe audio.
    
    Args:
        audio_file: Audio file
        language: Language code
        model: Model to use
    
    Returns:
        Transcription results
    """
    provider = get_stt_provider()
    return provider.transcribe_audio(audio_file, language, model)
