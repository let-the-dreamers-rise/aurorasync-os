"""
Slot Manager for AuroraSync OS.
Manages appointment slots across workshops with capacity and availability.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)


class SlotManager:
    """
    Manages appointment slots for workshops.
    """
    
    def __init__(self):
        """Initialize slot manager."""
        # Booked slots (in production, this would be in database)
        self.booked_slots: Dict[str, List[datetime]] = {}
        logger.info("Slot Manager initialized")
    
    def generate_slots(
        self,
        workshop_id: str,
        workshop_data: Dict[str, Any],
        start_date: datetime,
        days: int = 7,
        include_emergency: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Generate available slots for a workshop.
        
        Args:
            workshop_id: Workshop ID
            workshop_data: Workshop configuration
            start_date: Start date for slot generation
            days: Number of days to generate
            include_emergency: Include emergency slots
        
        Returns:
            List of available slots
        """
        slots = []
        
        # Parse operating hours
        start_hour = int(workshop_data["operating_hours"]["start"].split(":")[0])
        end_hour = int(workshop_data["operating_hours"]["end"].split(":")[0])
        
        # Get booked slots for this workshop
        booked = self.booked_slots.get(workshop_id, [])
        
        # Generate slots for each day
        for day_offset in range(days):
            current_date = start_date + timedelta(days=day_offset)
            
            # Skip if past date
            if current_date.date() < datetime.now().date():
                continue
            
            # Generate hourly slots
            for hour in range(start_hour, end_hour):
                # Morning slots (8-12)
                if start_hour <= hour < 12:
                    slot_type = "morning"
                # Afternoon slots (12-17)
                elif 12 <= hour < 17:
                    slot_type = "afternoon"
                # Evening slots (17-20)
                else:
                    slot_type = "evening"
                
                slot_time = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                # Check if slot is booked
                if slot_time in booked:
                    continue
                
                # Check if same day (today)
                is_same_day = slot_time.date() == datetime.now().date()
                
                # Check if emergency slot
                is_emergency = include_emergency and hour in [start_hour, start_hour + 1]
                
                # Calculate availability score
                availability_score = self._calculate_availability_score(
                    slot_time,
                    workshop_data,
                    len(booked)
                )
                
                slots.append({
                    "slot_time": slot_time.isoformat(),
                    "slot_type": slot_type,
                    "is_same_day": is_same_day,
                    "is_emergency": is_emergency,
                    "availability_score": availability_score,
                    "workshop_id": workshop_id,
                    "estimated_duration": 60,  # minutes
                    "technician_available": True
                })
        
        return slots
    
    def find_optimal_slot(
        self,
        workshop_id: str,
        workshop_data: Dict[str, Any],
        risk_level: str,
        owner_preferences: Optional[Dict[str, Any]] = None,
        is_emergency: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Find optimal slot based on risk level and preferences.
        
        Args:
            workshop_id: Workshop ID
            workshop_data: Workshop configuration
            risk_level: Risk level (low, medium, high)
            owner_preferences: Owner preferences (time, day)
            is_emergency: Whether this is an emergency
        
        Returns:
            Optimal slot or None
        """
        # Generate slots
        start_date = datetime.now()
        days = 1 if is_emergency else 7
        
        slots = self.generate_slots(
            workshop_id,
            workshop_data,
            start_date,
            days,
            include_emergency=is_emergency
        )
        
        if not slots:
            return None
        
        # Filter and score slots
        scored_slots = []
        
        for slot in slots:
            score = 0.0
            slot_time = datetime.fromisoformat(slot["slot_time"])
            
            # Emergency priority
            if is_emergency:
                if slot["is_same_day"]:
                    score += 100
                if slot["is_emergency"]:
                    score += 50
            
            # Risk-based urgency
            if risk_level == "high":
                # Prefer earlier slots
                days_away = (slot_time.date() - datetime.now().date()).days
                score += max(0, 50 - (days_away * 10))
            
            # Owner preferences
            if owner_preferences:
                pref_time = owner_preferences.get("preferred_time", "").lower()
                pref_day = owner_preferences.get("preferred_day", "").lower()
                
                # Time preference
                if pref_time and pref_time in slot["slot_type"]:
                    score += 30
                
                # Day preference
                if pref_day == "tomorrow" and days_away == 1:
                    score += 20
                elif pref_day == "today" and days_away == 0:
                    score += 40
                elif pref_day == "weekend" and slot_time.weekday() >= 5:
                    score += 25
            
            # Availability score
            score += slot["availability_score"] * 10
            
            scored_slots.append({
                **slot,
                "match_score": score
            })
        
        # Sort by score
        scored_slots.sort(key=lambda x: x["match_score"], reverse=True)
        
        return scored_slots[0] if scored_slots else None
    
    def book_slot(
        self,
        workshop_id: str,
        slot_time: datetime,
        vehicle_id: str,
        service_type: str
    ) -> Dict[str, Any]:
        """
        Book a slot.
        
        Args:
            workshop_id: Workshop ID
            slot_time: Slot time
            vehicle_id: Vehicle ID
            service_type: Service type
        
        Returns:
            Booking confirmation
        """
        # Add to booked slots
        if workshop_id not in self.booked_slots:
            self.booked_slots[workshop_id] = []
        
        self.booked_slots[workshop_id].append(slot_time)
        
        booking_id = f"BOOK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"Booked slot: {booking_id} for {vehicle_id} at {workshop_id} on {slot_time}")
        
        return {
            "booking_id": booking_id,
            "workshop_id": workshop_id,
            "slot_time": slot_time.isoformat(),
            "vehicle_id": vehicle_id,
            "service_type": service_type,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
    
    def _calculate_availability_score(
        self,
        slot_time: datetime,
        workshop_data: Dict[str, Any],
        booked_count: int
    ) -> float:
        """Calculate availability score for a slot."""
        score = 1.0
        
        # Reduce score based on how many slots are already booked
        capacity = workshop_data["technician_capacity"]
        if booked_count > capacity * 0.7:
            score *= 0.5
        
        # Prefer slots not too far in the future
        days_away = (slot_time.date() - datetime.now().date()).days
        if days_away > 3:
            score *= 0.8
        
        return score


# Global slot manager instance
_slot_manager = None


def get_slot_manager() -> SlotManager:
    """Get singleton slot manager instance."""
    global _slot_manager
    if _slot_manager is None:
        _slot_manager = SlotManager()
    return _slot_manager
