"""
Conversation Flow Manager for Voice Agent.
Manages multi-turn conversations and state.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from enum import Enum


logger = logging.getLogger(__name__)


class ConversationState(Enum):
    """Conversation states."""
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    WAITING_RESPONSE = "waiting_response"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class FlowManager:
    """
    Manages conversation flows and state.
    
    Handles:
    - Multi-turn conversations
    - State persistence
    - Branching logic
    - Timeout handling
    """
    
    def __init__(self):
        """Initialize flow manager."""
        # In-memory conversation storage
        # In production, this would use Redis or a database
        self.conversations: Dict[str, Dict[str, Any]] = {}
        self.conversation_timeout = timedelta(minutes=30)
        logger.info("Flow Manager initialized")
    
    def start_conversation(
        self,
        conversation_id: str,
        scenario: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Start a new conversation.
        
        Args:
            conversation_id: Unique conversation identifier
            scenario: Scenario type
            context: Initial context data
        
        Returns:
            Conversation state
        """
        conversation = {
            "conversation_id": conversation_id,
            "scenario": scenario,
            "state": ConversationState.INITIATED.value,
            "context": context,
            "turns": [],
            "current_turn": 0,
            "max_turns": context.get("max_turns", 5),
            "started_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + self.conversation_timeout).isoformat() + "Z"
        }
        
        self.conversations[conversation_id] = conversation
        logger.info(f"Started conversation: {conversation_id} (scenario: {scenario})")
        
        return conversation
    
    def add_turn(
        self,
        conversation_id: str,
        speaker: str,
        message: str,
        audio_metadata: Optional[Dict[str, Any]] = None,
        intent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a turn to the conversation.
        
        Args:
            conversation_id: Conversation ID
            speaker: Speaker ("agent" or "user")
            message: Message text
            audio_metadata: Audio metadata (optional)
            intent: Detected intent (optional)
        
        Returns:
            Updated conversation state
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation not found: {conversation_id}")
        
        conversation = self.conversations[conversation_id]
        
        turn = {
            "turn_number": len(conversation["turns"]) + 1,
            "speaker": speaker,
            "message": message,
            "audio_metadata": audio_metadata,
            "intent": intent,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        conversation["turns"].append(turn)
        conversation["current_turn"] = len(conversation["turns"])
        conversation["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        # Update state
        if speaker == "agent":
            conversation["state"] = ConversationState.WAITING_RESPONSE.value
        else:
            conversation["state"] = ConversationState.IN_PROGRESS.value
        
        logger.info(
            f"Added turn {turn['turn_number']} to conversation {conversation_id}: "
            f"{speaker} - {message[:50]}..."
        )
        
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get conversation state.
        
        Args:
            conversation_id: Conversation ID
        
        Returns:
            Conversation state or None
        """
        return self.conversations.get(conversation_id)
    
    def update_context(
        self,
        conversation_id: str,
        context_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update conversation context.
        
        Args:
            conversation_id: Conversation ID
            context_updates: Context updates
        
        Returns:
            Updated conversation state
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation not found: {conversation_id}")
        
        conversation = self.conversations[conversation_id]
        conversation["context"].update(context_updates)
        conversation["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        logger.info(f"Updated context for conversation {conversation_id}")
        
        return conversation
    
    def should_continue(self, conversation_id: str) -> bool:
        """
        Check if conversation should continue.
        
        Args:
            conversation_id: Conversation ID
        
        Returns:
            True if conversation should continue
        """
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            return False
        
        # Check if max turns reached
        if conversation["current_turn"] >= conversation["max_turns"]:
            logger.info(f"Conversation {conversation_id} reached max turns")
            return False
        
        # Check if expired
        expires_at = datetime.fromisoformat(conversation["expires_at"].replace("Z", ""))
        if datetime.utcnow() > expires_at:
            logger.info(f"Conversation {conversation_id} expired")
            return False
        
        # Check state
        if conversation["state"] in [
            ConversationState.COMPLETED.value,
            ConversationState.FAILED.value,
            ConversationState.ABANDONED.value
        ]:
            return False
        
        return True
    
    def complete_conversation(
        self,
        conversation_id: str,
        outcome: str,
        summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark conversation as completed.
        
        Args:
            conversation_id: Conversation ID
            outcome: Outcome ("success", "declined", "abandoned")
            summary: Optional summary
        
        Returns:
            Final conversation state
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation not found: {conversation_id}")
        
        conversation = self.conversations[conversation_id]
        conversation["state"] = ConversationState.COMPLETED.value
        conversation["outcome"] = outcome
        conversation["summary"] = summary
        conversation["completed_at"] = datetime.utcnow().isoformat() + "Z"
        conversation["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        logger.info(f"Completed conversation {conversation_id}: {outcome}")
        
        return conversation
    
    def get_next_action(
        self,
        conversation_id: str,
        user_response: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Determine next action based on conversation state.
        
        Args:
            conversation_id: Conversation ID
            user_response: User's last response (optional)
        
        Returns:
            Next action configuration
        """
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            return {
                "action": "error",
                "message": "Conversation not found"
            }
        
        # Check if should continue
        if not self.should_continue(conversation_id):
            return {
                "action": "end",
                "message": "Conversation ended"
            }
        
        # Analyze user response if provided
        if user_response:
            response_lower = user_response.lower()
            
            # Positive responses
            if any(word in response_lower for word in ["yes", "ok", "sure", "book"]):
                return {
                    "action": "confirm",
                    "next_scenario": None,
                    "message": "Proceeding with confirmation"
                }
            
            # Negative responses
            elif any(word in response_lower for word in ["no", "not now", "later"]):
                return {
                    "action": "offer_alternatives",
                    "next_scenario": "booking_recovery",
                    "message": "Offering alternative options"
                }
            
            # Safety inquiry
            elif any(word in response_lower for word in ["safe", "drive", "risk"]):
                return {
                    "action": "provide_safety_info",
                    "next_scenario": "safety_check",
                    "message": "Providing safety information"
                }
            
            # Cost inquiry
            elif any(word in response_lower for word in ["cost", "price", "expensive"]):
                return {
                    "action": "provide_cost_info",
                    "next_scenario": "cost_inquiry",
                    "message": "Providing cost information"
                }
        
        # Default: continue conversation
        return {
            "action": "continue",
            "next_scenario": None,
            "message": "Continuing conversation"
        }
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired conversations.
        
        Returns:
            Number of conversations cleaned up
        """
        now = datetime.utcnow()
        expired = []
        
        for conv_id, conversation in self.conversations.items():
            expires_at = datetime.fromisoformat(conversation["expires_at"].replace("Z", ""))
            if now > expires_at:
                expired.append(conv_id)
        
        for conv_id in expired:
            del self.conversations[conv_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired conversations")
        
        return len(expired)
    
    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get conversation summary.
        
        Args:
            conversation_id: Conversation ID
        
        Returns:
            Conversation summary
        """
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            return {"error": "Conversation not found"}
        
        return {
            "conversation_id": conversation_id,
            "scenario": conversation["scenario"],
            "state": conversation["state"],
            "turn_count": len(conversation["turns"]),
            "started_at": conversation["started_at"],
            "updated_at": conversation["updated_at"],
            "outcome": conversation.get("outcome"),
            "summary": conversation.get("summary")
        }


# Global flow manager instance
_flow_manager = None


def get_flow_manager() -> FlowManager:
    """Get singleton flow manager instance."""
    global _flow_manager
    if _flow_manager is None:
        _flow_manager = FlowManager()
    return _flow_manager
