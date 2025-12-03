"""
Voice Agent for AuroraSync OS.
Handles voice-based customer interactions.
"""

from typing import Dict, Any, Optional
import uuid
import logging

from app.agents.base_agent import BaseAgent
from app.voice_engine.message_templates import MessageTemplates
from app.voice_engine.conversation_scenarios import ConversationScenarios
from app.voice_engine.tts_provider import get_tts_provider
from app.voice_engine.stt_provider import get_stt_provider
from app.voice_engine.flow_manager import get_flow_manager


logger = logging.getLogger(__name__)


class VoiceAgent(BaseAgent):
    """
    Voice Agent for conversational AI interactions.
    
    Handles:
    - Voice-based customer engagement
    - Multi-turn conversations
    - TTS/STT integration
    - Scenario-based flows
    """
    
    def __init__(self):
        """Initialize Voice Agent."""
        super().__init__(name="voice")
        
        # Initialize providers
        self.tts_provider = get_tts_provider()
        self.stt_provider = get_stt_provider()
        self.flow_manager = get_flow_manager()
        
        self.logger.info("🎤 Voice Agent ready with TTS/STT support")
    
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle voice agent events.
        
        Args:
            event: Event to process
        
        Returns:
            Response with text and audio
        """
        self.log_event(event, "received")
        
        event_type = event.get("type", "unknown")
        payload = event.get("payload", {})
        
        # Route to appropriate handler
        if event_type == "voice_predict_failure":
            return self._handle_predict_failure(payload)
        
        elif event_type == "voice_urgent_alert":
            return self._handle_urgent_alert(payload)
        
        elif event_type == "voice_reminder":
            return self._handle_reminder(payload)
        
        elif event_type == "voice_feedback":
            return self._handle_feedback(payload)
        
        elif event_type == "voice_booking_recovery":
            return self._handle_booking_recovery(payload)
        
        elif event_type == "voice_transcribe":
            return self._handle_transcribe(payload)
        
        elif event_type == "voice_continue":
            return self._handle_continue_conversation(payload)
        
        # Default response
        return self.create_response(
            status="success",
            result={"note": f"Voice Agent processed: {event_type}"}
        )
    
    def _handle_predict_failure(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle predicted failure scenario."""
        # Extract data
        vehicle_data = payload.get("vehicle_data", {})
        prediction_data = payload.get("prediction_data", {})
        booking_data = payload.get("booking_data", {})
        
        # Determine risk level and tone
        risk_level = prediction_data.get("risk_level", "medium")
        tone = "urgent" if risk_level == "high" else "polite"
        
        # Get scenario configuration
        scenario_config = ConversationScenarios.get_scenario_config(
            "predicted_failure",
            risk_level
        )
        
        # Build context
        context = ConversationScenarios.get_context_for_scenario(
            "predicted_failure",
            vehicle_data,
            prediction_data,
            booking_data
        )
        
        # Generate message
        message = MessageTemplates.build_full_message(
            "predicted_failure",
            tone,
            context
        )
        
        # Generate TTS
        audio = self.tts_provider.generate_tts(
            message,
            voice=scenario_config["voice"],
            speaking_rate=scenario_config["speaking_rate"]
        )
        
        # Start conversation flow
        conversation_id = str(uuid.uuid4())
        conversation = self.flow_manager.start_conversation(
            conversation_id,
            "predicted_failure",
            {**context, **scenario_config}
        )
        
        # Add agent turn
        self.flow_manager.add_turn(
            conversation_id,
            "agent",
            message,
            audio
        )
        
        return self.create_response(
            status="success",
            result={
                "conversation_id": conversation_id,
                "scenario": "predicted_failure",
                "tone": tone,
                "text": message,
                "audio": audio,
                "context": context,
                "next_expected_responses": scenario_config["expected_responses"]
            }
        )
    
    def _handle_urgent_alert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle urgent alert scenario."""
        vehicle_data = payload.get("vehicle_data", {})
        prediction_data = payload.get("prediction_data", {})
        booking_data = payload.get("booking_data", {})
        
        # Force urgent tone
        scenario_config = ConversationScenarios.get_scenario_config(
            "urgent_alert",
            "high"
        )
        
        context = ConversationScenarios.get_context_for_scenario(
            "predicted_failure",
            vehicle_data,
            prediction_data,
            booking_data
        )
        
        message = MessageTemplates.build_full_message(
            "predicted_failure",
            "urgent",
            context
        )
        
        audio = self.tts_provider.generate_tts(
            message,
            voice=scenario_config["voice"],
            speaking_rate=scenario_config["speaking_rate"]
        )
        
        conversation_id = str(uuid.uuid4())
        self.flow_manager.start_conversation(
            conversation_id,
            "urgent_alert",
            {**context, **scenario_config}
        )
        
        self.flow_manager.add_turn(conversation_id, "agent", message, audio)
        
        return self.create_response(
            status="success",
            result={
                "conversation_id": conversation_id,
                "scenario": "urgent_alert",
                "tone": "urgent",
                "text": message,
                "audio": audio,
                "priority": "critical"
            }
        )
    
    def _handle_reminder(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle appointment reminder scenario."""
        vehicle_data = payload.get("vehicle_data", {})
        booking_data = payload.get("booking_data", {})
        
        scenario_config = ConversationScenarios.get_scenario_config(
            "appointment_reminder"
        )
        
        context = ConversationScenarios.get_context_for_scenario(
            "appointment_reminder",
            vehicle_data,
            None,
            booking_data
        )
        
        message = MessageTemplates.build_full_message(
            "appointment_reminder",
            "friendly",
            context
        )
        
        audio = self.tts_provider.generate_tts(
            message,
            voice=scenario_config["voice"]
        )
        
        conversation_id = str(uuid.uuid4())
        self.flow_manager.start_conversation(
            conversation_id,
            "appointment_reminder",
            {**context, **scenario_config}
        )
        
        self.flow_manager.add_turn(conversation_id, "agent", message, audio)
        
        return self.create_response(
            status="success",
            result={
                "conversation_id": conversation_id,
                "scenario": "appointment_reminder",
                "text": message,
                "audio": audio
            }
        )
    
    def _handle_feedback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle post-service feedback scenario."""
        vehicle_data = payload.get("vehicle_data", {})
        service_data = payload.get("service_data", {})
        
        scenario_config = ConversationScenarios.get_scenario_config(
            "post_service_feedback"
        )
        
        context = ConversationScenarios.get_context_for_scenario(
            "post_service_feedback",
            vehicle_data,
            None,
            service_data
        )
        
        message = MessageTemplates.build_full_message(
            "post_service_feedback",
            "friendly",
            context
        )
        
        audio = self.tts_provider.generate_tts(
            message,
            voice=scenario_config["voice"]
        )
        
        conversation_id = str(uuid.uuid4())
        self.flow_manager.start_conversation(
            conversation_id,
            "post_service_feedback",
            {**context, **scenario_config}
        )
        
        self.flow_manager.add_turn(conversation_id, "agent", message, audio)
        
        return self.create_response(
            status="success",
            result={
                "conversation_id": conversation_id,
                "scenario": "post_service_feedback",
                "text": message,
                "audio": audio
            }
        )
    
    def _handle_booking_recovery(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle booking recovery scenario."""
        vehicle_data = payload.get("vehicle_data", {})
        prediction_data = payload.get("prediction_data", {})
        booking_data = payload.get("booking_data", {})
        
        scenario_config = ConversationScenarios.get_scenario_config(
            "booking_recovery"
        )
        
        context = ConversationScenarios.get_context_for_scenario(
            "booking_recovery",
            vehicle_data,
            prediction_data,
            booking_data
        )
        
        # Add alternate slots
        context["alternate_slots"] = "tomorrow morning at 9 AM, tomorrow afternoon at 2 PM, or this Saturday at 10 AM"
        
        message = MessageTemplates.build_full_message(
            "booking_recovery",
            "friendly",
            context
        )
        
        audio = self.tts_provider.generate_tts(
            message,
            voice=scenario_config["voice"],
            speaking_rate=scenario_config["speaking_rate"]
        )
        
        conversation_id = str(uuid.uuid4())
        self.flow_manager.start_conversation(
            conversation_id,
            "booking_recovery",
            {**context, **scenario_config}
        )
        
        self.flow_manager.add_turn(conversation_id, "agent", message, audio)
        
        return self.create_response(
            status="success",
            result={
                "conversation_id": conversation_id,
                "scenario": "booking_recovery",
                "text": message,
                "audio": audio
            }
        )
    
    def _handle_transcribe(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle audio transcription."""
        audio_file = payload.get("audio_file")
        language = payload.get("language", "en-IN")
        
        # Transcribe audio
        transcription = self.stt_provider.transcribe_audio(audio_file, language)
        
        # Detect intent
        intent_result = self.stt_provider.detect_intent(transcription["text"])
        
        return self.create_response(
            status="success",
            result={
                "transcription": transcription,
                "intent": intent_result
            }
        )
    
    def _handle_continue_conversation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle conversation continuation."""
        conversation_id = payload.get("conversation_id")
        user_response = payload.get("user_response")
        
        if not conversation_id:
            return self.create_response(
                status="error",
                error="conversation_id required"
            )
        
        # Get conversation
        conversation = self.flow_manager.get_conversation(conversation_id)
        if not conversation:
            return self.create_response(
                status="error",
                error="Conversation not found"
            )
        
        # Add user turn
        if user_response:
            self.flow_manager.add_turn(
                conversation_id,
                "user",
                user_response
            )
        
        # Get next action
        next_action = self.flow_manager.get_next_action(
            conversation_id,
            user_response
        )
        
        # Generate response based on action
        if next_action["action"] == "confirm":
            message = "Great! I'll proceed with booking that appointment for you. You'll receive a confirmation shortly."
        elif next_action["action"] == "offer_alternatives":
            message = "I understand. Let me offer you some alternative time slots that might work better."
        elif next_action["action"] == "provide_safety_info":
            context = conversation["context"]
            risk_level = context.get("risk_level", "medium")
            templates = MessageTemplates.get_template("safety_check", "technical")
            message = templates.get(risk_level, templates.get("medium_risk", "")).safe_substitute(context)
        else:
            message = "How else can I help you today?"
        
        # Generate TTS
        audio = self.tts_provider.generate_tts(message)
        
        # Add agent turn
        self.flow_manager.add_turn(
            conversation_id,
            "agent",
            message,
            audio
        )
        
        return self.create_response(
            status="success",
            result={
                "conversation_id": conversation_id,
                "action": next_action["action"],
                "text": message,
                "audio": audio,
                "should_continue": self.flow_manager.should_continue(conversation_id)
            }
        )
