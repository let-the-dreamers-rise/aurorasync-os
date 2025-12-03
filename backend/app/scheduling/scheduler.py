"""
Main Scheduler for AuroraSync OS.
Orchestrates intelligent appointment scheduling with load balancing and escalation.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

from app.scheduling.workshop_manager import get_workshop_manager
from app.scheduling.slot_manager import get_slot_manager
from app.scheduling.demand_forecaster import get_demand_forecaster
from app.scheduling.escalation_engine import get_escalation_engine


logger = logging.getLogger(__name__)


class Scheduler:
    """
    Main scheduling orchestrator.
    Combines workshop selection, slot optimization, demand forecasting, and escalation.
    """
    
    def __init__(self):
        """Initialize scheduler."""
        self.workshop_manager = get_workshop_manager()
        self.slot_manager = get_slot_manager()
        self.demand_forecaster = get_demand_forecaster()
        self.escalation_engine = get_escalation_engine()
        self.booking_count = 0
        logger.info("🗓️  Scheduler initialized")
    
    def schedule_appointment(
        self,
        vehicle_id: str,
        component: str,
        risk_level: str,
        probability: float,
        owner_preferences: Optional[Dict[str, Any]] = None,
        vehicle_location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Schedule an appointment with intelligent optimization.
        
        Args:
            vehicle_id: Vehicle ID
            component: Component needing service
            risk_level: Risk level (low, medium, high)
            probability: Failure probability (0.0 to 1.0)
            owner_preferences: Owner preferences (time, day, city)
            vehicle_location: Vehicle location/city
        
        Returns:
            Scheduling result with workshop, slot, and reasoning
        """
        self.booking_count += 1
        logger.info(
            f"Scheduling request #{self.booking_count}: {vehicle_id} - "
            f"{component} ({risk_level}, {probability:.2f})"
        )
        
        # Step 1: Evaluate escalation
        escalation = self.escalation_engine.evaluate_escalation(
            risk_level,
            component,
            probability
        )
        
        is_emergency = escalation["severity"] in ["CRITICAL", "EMERGENCY"]
        should_override = escalation["override_preferences"]
        
        logger.info(f"Escalation: {escalation['severity']} - {escalation['reasoning']}")
        
        # Step 2: Find best workshop
        preferred_city = None
        if owner_preferences and not should_override:
            preferred_city = owner_preferences.get("preferred_city")
        if not preferred_city and vehicle_location:
            preferred_city = vehicle_location
        
        workshop_selection = self.workshop_manager.find_best_workshop(
            component,
            risk_level,
            is_emergency,
            preferred_city
        )
        
        workshop_id = workshop_selection["workshop_id"]
        workshop_data = workshop_selection["workshop_data"]
        
        logger.info(f"Selected workshop: {workshop_id} - {workshop_selection['reasoning']}")
        
        # Step 3: Get demand forecast
        demand_forecast = self.demand_forecaster.predict_optimal_slot(
            workshop_id,
            component,
            risk_level
        )
        
        # Step 4: Find optimal slot
        slot = self.slot_manager.find_optimal_slot(
            workshop_id,
            workshop_data,
            risk_level,
            owner_preferences if not should_override else None,
            is_emergency
        )
        
        if not slot:
            return {
                "status": "error",
                "error": "No available slots found",
                "workshop_id": workshop_id
            }
        
        # Step 5: Book the slot
        slot_time = datetime.fromisoformat(slot["slot_time"])
        booking = self.slot_manager.book_slot(
            workshop_id,
            slot_time,
            vehicle_id,
            component
        )
        
        # Step 6: Update workshop load
        load_delta = 0.1 if not is_emergency else 0.15
        self.workshop_manager.update_load(workshop_id, load_delta)
        
        # Step 7: Use emergency slot if needed
        if is_emergency:
            self.workshop_manager.use_emergency_slot(workshop_id)
        
        # Step 8: Generate comprehensive response
        return {
            "status": "success",
            "booking_id": booking["booking_id"],
            "assigned_workshop": {
                "id": workshop_id,
                "name": workshop_data["name"],
                "city": workshop_data["city"],
                "address": f"{workshop_data['name']}, {workshop_data['city']}",
                "phone": "+91-1800-XXX-XXXX",
                "rating": workshop_data["rating"]
            },
            "slot": {
                "date": slot_time.strftime("%Y-%m-%d"),
                "time": slot_time.strftime("%H:%M"),
                "datetime": slot["slot_time"],
                "type": slot["slot_type"],
                "is_emergency": is_emergency,
                "estimated_duration": 60
            },
            "priority": escalation["severity"],
            "escalation": {
                "severity": escalation["severity"],
                "should_escalate": escalation["should_escalate"],
                "recommended_timeframe": escalation["recommended_timeframe"],
                "actions": escalation["actions"],
                "escalation_id": escalation.get("escalation_id")
            },
            "reasoning": {
                "workshop_selection": workshop_selection["reasoning"],
                "escalation": escalation["reasoning"],
                "demand_forecast": demand_forecast["reasoning"],
                "slot_match_score": slot.get("match_score", 0)
            },
            "safety_assessment": self.escalation_engine.check_safety_to_drive(
                component,
                probability,
                escalation["severity"]
            ),
            "demand_forecast": demand_forecast,
            "preferences_honored": not should_override,
            "created_at": datetime.now().isoformat()
        }


# Global scheduler instance
_scheduler = None


def get_scheduler() -> Scheduler:
    """Get singleton scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = Scheduler()
    return _scheduler


def schedule_appointment(
    vehicle_id: str,
    component: str,
    risk_level: str,
    probability: float,
    owner_preferences: Optional[Dict[str, Any]] = None,
    vehicle_location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to schedule an appointment.
    
    Args:
        vehicle_id: Vehicle ID
        component: Component needing service
        risk_level: Risk level
        probability: Failure probability
        owner_preferences: Owner preferences
        vehicle_location: Vehicle location
    
    Returns:
        Scheduling result
    """
    scheduler = get_scheduler()
    return scheduler.schedule_appointment(
        vehicle_id,
        component,
        risk_level,
        probability,
        owner_preferences,
        vehicle_location
    )
