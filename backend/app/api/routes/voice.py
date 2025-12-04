"""
Voice API routes for AuroraSync OS.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging

from app.voice_engine.voice_agent import VoiceAgent
from app.voice_engine.tts_provider import get_tts_provider
from app.voice_engine.stt_provider import get_stt_provider
from app.voice_engine.flow_manager import get_flow_manager


router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize voice agent
_voice_agent = None


def get_voice_agent() -> VoiceAgent:
    """Get singleton voice agent instance."""
    global _voice_agent
    if _voice_agent is None:
        _voice_agent = VoiceAgent()
    return _voice_agent


class VoiceEngageRequest(BaseModel):
    """Request model for voice engagement."""
    scenario: str = Field(..., description="Scenario type (predicted_failure, urgent_alert, etc.)")
    vehicle_data: Dict[str, Any] = Field(..., description="Vehicle information")
    prediction_data: Optional[Dict[str, Any]] = Field(None, description="ML prediction data")
    booking_data: Optional[Dict[str, Any]] = Field(None, description="Booking information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "predicted_failure",
                "vehicle_data": {
                    "vehicle_id": "VEH001",
                    "owner_name": "Rahul",
                    "model": "Honda Accord",
                    "make": "Honda"
                },
                "prediction_data": {
                    "component": "brake_system",
                    "probability": 0.85,
                    "risk_level": "high"
                },
                "booking_data": {
                    "workshop_name": "AutoCare Mumbai",
                    "recommended_slot": "tomorrow at 10 AM"
                }
            }
        }


class VoiceContinueRequest(BaseModel):
    """Request model for continuing conversation."""
    conversation_id: str = Field(..., description="Conversation ID")
    user_response: str = Field(..., description="User's response")


@router.post("/engage", tags=["Voice"])
def engage_voice(request: VoiceEngageRequest) -> Dict[str, Any]:
    """
    Start a voice conversation with the customer.
    
    This endpoint initiates a voice-based conversation for various scenarios:
    - **predicted_failure**: Notify about predicted vehicle failure
    - **urgent_alert**: Critical alert requiring immediate action
    - **appointment_reminder**: Remind about upcoming service
    - **post_service_feedback**: Collect feedback after service
    - **booking_recovery**: Recover from declined appointment
    
    The response includes:
    - Text message
    - Audio metadata (TTS generated)
    - Conversation ID for multi-turn conversations
    - Expected user responses
    
    Args:
        request: Voice engagement request
    
    Returns:
        Voice conversation response with text and audio
    
    Raises:
        HTTPException: If engagement fails
    """
    try:
        voice_agent = get_voice_agent()
        
        # Map scenario to event type
        event_type_map = {
            "predicted_failure": "voice_predict_failure",
            "urgent_alert": "voice_urgent_alert",
            "appointment_reminder": "voice_reminder",
            "post_service_feedback": "voice_feedback",
            "booking_recovery": "voice_booking_recovery"
        }
        
        event_type = event_type_map.get(request.scenario, "voice_predict_failure")
        
        # Create event
        event = {
            "type": event_type,
            "payload": {
                "vehicle_data": request.vehicle_data,
                "prediction_data": request.prediction_data,
                "booking_data": request.booking_data
            }
        }
        
        # Handle event
        response = voice_agent.handle_event(event)
        
        # Extract result from BaseAgent response format
        if isinstance(response, dict) and "result" in response:
            result = response["result"]
            # Ensure 'message' field exists (frontend expects 'message', backend returns 'text')
            if "text" in result and "message" not in result:
                result["message"] = result["text"]
            return result
        
        return response
    
    except Exception as e:
        import traceback
        error_detail = f"Voice engagement failed: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_detail)
        raise HTTPException(
            status_code=500,
            detail=f"Voice engagement failed: {str(e)}"
        )


@router.post("/continue", tags=["Voice"])
def continue_conversation(request: VoiceContinueRequest) -> Dict[str, Any]:
    """
    Continue an ongoing voice conversation.
    
    Use this endpoint to handle multi-turn conversations.
    Provide the conversation ID and the user's response.
    
    Args:
        request: Continue conversation request
    
    Returns:
        Next turn in the conversation
    
    Raises:
        HTTPException: If conversation not found or continuation fails
    """
    try:
        voice_agent = get_voice_agent()
        
        event = {
            "type": "voice_continue",
            "payload": {
                "conversation_id": request.conversation_id,
                "user_response": request.user_response
            }
        }
        
        response = voice_agent.handle_event(event)
        
        # Extract result from BaseAgent response format
        if isinstance(response, dict) and "result" in response:
            result = response["result"]
            # Ensure 'message' field exists (frontend expects 'message', backend returns 'text')
            if "text" in result and "message" not in result:
                result["message"] = result["text"]
            # Check if conversation is complete
            if "should_continue" in result:
                result["conversation_complete"] = not result["should_continue"]
            return result
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Conversation continuation failed: {str(e)}"
        )


@router.post("/transcribe", tags=["Voice"])
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = "en-IN"
) -> Dict[str, Any]:
    """
    Transcribe audio to text.
    
    Upload an audio file and get the transcribed text.
    Also includes intent detection.
    
    Args:
        audio: Audio file (WAV, MP3, etc.)
        language: Language code (default: en-IN)
    
    Returns:
        Transcription results with intent detection
    
    Raises:
        HTTPException: If transcription fails
    """
    try:
        stt_provider = get_stt_provider()
        
        # In production, we would read the actual audio file
        # For demo, we use mock transcription
        transcription = stt_provider.transcribe_audio(audio.file, language)
        
        # Detect intent
        intent = stt_provider.detect_intent(transcription["text"])
        
        return {
            "status": "success",
            "transcription": transcription,
            "intent": intent
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )


@router.get("/conversation/{conversation_id}", tags=["Voice"])
def get_conversation(conversation_id: str) -> Dict[str, Any]:
    """
    Get conversation details.
    
    Retrieve the full conversation history and state.
    
    Args:
        conversation_id: Conversation ID
    
    Returns:
        Conversation details
    
    Raises:
        HTTPException: If conversation not found
    """
    try:
        flow_manager = get_flow_manager()
        conversation = flow_manager.get_conversation(conversation_id)
        
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        
        return {
            "status": "success",
            "conversation": conversation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversation: {str(e)}"
        )


@router.get("/voices", tags=["Voice"])
def get_available_voices() -> Dict[str, Any]:
    """
    Get list of available TTS voices.
    
    Returns:
        Available voices with metadata
    """
    tts_provider = get_tts_provider()
    voices = tts_provider.get_available_voices()
    
    return {
        "status": "success",
        "voices": voices,
        "count": len(voices)
    }


@router.post("/tts", tags=["Voice"])
def generate_speech(
    text: str,
    voice: str = "Aurora_Default",
    speaking_rate: float = 1.0
) -> Dict[str, Any]:
    """
    Generate speech from text.
    
    Convert text to speech using specified voice.
    
    Args:
        text: Text to convert
        voice: Voice to use
        speaking_rate: Speaking rate (0.5 to 2.0)
    
    Returns:
        Audio metadata
    
    Raises:
        HTTPException: If TTS generation fails
    """
    try:
        tts_provider = get_tts_provider()
        audio = tts_provider.generate_tts(text, voice, speaking_rate)
        
        return {
            "status": "success",
            "audio": audio
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"TTS generation failed: {str(e)}"
        )


@router.get("/audio/{audio_id}", tags=["Voice"])
def get_audio(audio_id: str) -> Dict[str, Any]:
    """
    Get audio file.
    
    In production, this would serve the actual audio file.
    For demo, returns metadata.
    
    Args:
        audio_id: Audio ID
    
    Returns:
        Audio metadata or file
    """
    return {
        "status": "success",
        "audio_id": audio_id,
        "message": "Mock audio endpoint - in production, this would serve the actual audio file",
        "format": "wav",
        "sample_rate": 24000
    }
