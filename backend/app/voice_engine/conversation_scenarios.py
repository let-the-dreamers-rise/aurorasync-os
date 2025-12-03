"""
Conversation Scenarios for Voice Agent.
Defines conversation flows and branching logic.
"""

from typing import Dict, Any, List, Optional
from enum import Enum


class ScenarioType(Enum):
    """Enumeration of conversation scenarios."""
    PREDICTED_FAILURE = "predicted_failure"
    URGENT_ALERT = "urgent_alert"
    APPOINTMENT_REMINDER = "appointment_reminder"
    BOOKING_RECOVERY = "booking_recovery"
    POST_SERVICE_FEEDBACK = "post_service_feedback"
    SAFETY_CHECK = "safety_check"
    COST_INQUIRY = "cost_inquiry"


class ToneType(Enum):
    """Enumeration of conversation tones."""
    POLITE = "polite"
    URGENT = "urgent"
    TECHNICAL = "technical"
    FRIENDLY = "friendly"
    EMPATHETIC = "empathetic"


class ConversationScenarios:
    """
    Manages conversation scenarios and their configurations.
    """
    
    @staticmethod
    def get_scenario_config(scenario: str, risk_level: str = "medium") -> Dict[str, Any]:
        """
        Get configuration for a conversation scenario.
        
        Args:
            scenario: Scenario type
            risk_level: Risk level (low, medium, high)
        
        Returns:
            Scenario configuration
        """
        configs = {
            "predicted_failure": {
                "tone": "urgent" if risk_level == "high" else "polite",
                "max_turns": 5,
                "requires_confirmation": True,
                "fallback_scenarios": ["booking_recovery", "safety_check"],
                "expected_responses": [
                    "yes", "no", "not now", "tell me more",
                    "is it safe", "how much", "when"
                ],
                "voice": "Aurora_Indian_Female",
                "speaking_rate": 1.0 if risk_level != "high" else 1.1,
                "priority": "high" if risk_level == "high" else "medium"
            },
            
            "urgent_alert": {
                "tone": "urgent",
                "max_turns": 3,
                "requires_confirmation": True,
                "fallback_scenarios": ["safety_check"],
                "expected_responses": ["yes", "no", "what should I do"],
                "voice": "Aurora_Urgent_Alert",
                "speaking_rate": 1.2,
                "priority": "critical"
            },
            
            "appointment_reminder": {
                "tone": "friendly",
                "max_turns": 3,
                "requires_confirmation": True,
                "fallback_scenarios": ["booking_recovery"],
                "expected_responses": ["yes", "no", "reschedule", "cancel"],
                "voice": "Aurora_Default",
                "speaking_rate": 1.0,
                "priority": "low"
            },
            
            "booking_recovery": {
                "tone": "empathetic",
                "max_turns": 5,
                "requires_confirmation": True,
                "fallback_scenarios": ["cost_inquiry"],
                "expected_responses": [
                    "morning", "afternoon", "evening", "weekend",
                    "next week", "not interested"
                ],
                "voice": "Aurora_Indian_Female",
                "speaking_rate": 0.95,
                "priority": "medium"
            },
            
            "post_service_feedback": {
                "tone": "friendly",
                "max_turns": 4,
                "requires_confirmation": False,
                "fallback_scenarios": [],
                "expected_responses": [
                    "1", "2", "3", "4", "5",
                    "satisfied", "not satisfied", "issue resolved"
                ],
                "voice": "Aurora_Default",
                "speaking_rate": 1.0,
                "priority": "low"
            },
            
            "safety_check": {
                "tone": "technical",
                "max_turns": 2,
                "requires_confirmation": False,
                "fallback_scenarios": ["predicted_failure"],
                "expected_responses": ["ok", "understood", "what next"],
                "voice": "Aurora_Indian_Male",
                "speaking_rate": 0.9,
                "priority": "high"
            },
            
            "cost_inquiry": {
                "tone": "technical",
                "max_turns": 3,
                "requires_confirmation": False,
                "fallback_scenarios": ["predicted_failure"],
                "expected_responses": [
                    "ok", "too expensive", "any discount",
                    "payment options", "proceed"
                ],
                "voice": "Aurora_Indian_Male",
                "speaking_rate": 0.95,
                "priority": "medium"
            }
        }
        
        return configs.get(scenario, configs["predicted_failure"])
    
    @staticmethod
    def get_context_for_scenario(
        scenario: str,
        vehicle_data: Dict[str, Any],
        prediction_data: Optional[Dict[str, Any]] = None,
        booking_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build context dictionary for a scenario.
        
        Args:
            scenario: Scenario type
            vehicle_data: Vehicle information
            prediction_data: ML prediction data (optional)
            booking_data: Booking information (optional)
        
        Returns:
            Context dictionary for template rendering
        """
        # Base context
        context = {
            "owner_name": vehicle_data.get("owner_name", "Customer"),
            "vehicle_id": vehicle_data.get("vehicle_id", "Unknown"),
            "vehicle_model": vehicle_data.get("model", "your vehicle"),
            "vehicle_make": vehicle_data.get("make", ""),
        }
        
        # Add prediction data if available
        if prediction_data:
            context.update({
                "component": prediction_data.get("component", "system"),
                "probability": int(prediction_data.get("probability", 0) * 100),
                "risk_level": prediction_data.get("risk_level", "medium"),
                "timeframe": ConversationScenarios._get_timeframe(
                    prediction_data.get("probability", 0)
                ),
            })
        
        # Add booking data if available
        if booking_data:
            context.update({
                "workshop_name": booking_data.get("workshop_name", "our service center"),
                "workshop_phone": booking_data.get("workshop_phone", "1800-XXX-XXXX"),
                "recommended_slot": booking_data.get("recommended_slot", "soon"),
                "appointment_date": booking_data.get("appointment_date", ""),
                "appointment_time": booking_data.get("appointment_time", ""),
                "service_type": booking_data.get("service_type", "inspection"),
                "duration": booking_data.get("duration", "60"),
            })
        
        # Add cost estimates
        if prediction_data:
            component = prediction_data.get("component", "system")
            context.update(ConversationScenarios._get_cost_estimate(component))
        
        return context
    
    @staticmethod
    def _get_timeframe(probability: float) -> str:
        """Get timeframe based on failure probability."""
        if probability >= 0.8:
            return "24-48 hours"
        elif probability >= 0.5:
            return "3-7 days"
        elif probability >= 0.3:
            return "1-2 weeks"
        else:
            return "2-4 weeks"
    
    @staticmethod
    def _get_cost_estimate(component: str) -> Dict[str, Any]:
        """Get cost estimate for a component."""
        estimates = {
            "brake_system": {
                "cost_min": 3000,
                "cost_max": 8000,
                "parts_cost": 4000,
                "labor_cost": 2000,
                "diagnostic_cost": 500,
                "savings": 15000,
                "warranty_period": "6 months"
            },
            "engine": {
                "cost_min": 10000,
                "cost_max": 50000,
                "parts_cost": 30000,
                "labor_cost": 15000,
                "diagnostic_cost": 1000,
                "savings": 100000,
                "warranty_period": "1 year"
            },
            "battery": {
                "cost_min": 5000,
                "cost_max": 15000,
                "parts_cost": 8000,
                "labor_cost": 2000,
                "diagnostic_cost": 500,
                "savings": 5000,
                "warranty_period": "1 year"
            },
            "tyre": {
                "cost_min": 4000,
                "cost_max": 20000,
                "parts_cost": 12000,
                "labor_cost": 2000,
                "diagnostic_cost": 500,
                "savings": 10000,
                "warranty_period": "6 months"
            }
        }
        
        return estimates.get(component, estimates["brake_system"])
    
    @staticmethod
    def get_response_branches(scenario: str, user_response: str) -> Dict[str, Any]:
        """
        Get next action based on user response.
        
        Args:
            scenario: Current scenario
            user_response: User's response (normalized)
        
        Returns:
            Next action configuration
        """
        response_lower = user_response.lower().strip()
        
        # Predicted failure responses
        if scenario == "predicted_failure":
            if any(word in response_lower for word in ["yes", "ok", "sure", "book"]):
                return {
                    "action": "confirm_booking",
                    "next_scenario": None,
                    "message": "Great! I'll book that appointment for you."
                }
            elif any(word in response_lower for word in ["no", "not now", "later"]):
                return {
                    "action": "offer_alternatives",
                    "next_scenario": "booking_recovery",
                    "message": "I understand. Let me offer some alternative times."
                }
            elif any(word in response_lower for word in ["safe", "drive"]):
                return {
                    "action": "safety_info",
                    "next_scenario": "safety_check",
                    "message": "Let me explain the safety implications."
                }
            elif any(word in response_lower for word in ["cost", "price", "expensive"]):
                return {
                    "action": "cost_info",
                    "next_scenario": "cost_inquiry",
                    "message": "Let me break down the estimated costs."
                }
        
        # Default: continue conversation
        return {
            "action": "continue",
            "next_scenario": None,
            "message": "I understand. How can I help you further?"
        }
