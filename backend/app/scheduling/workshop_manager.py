"""
Workshop Manager for AuroraSync OS.
Manages multiple service centers with capacity, load, and availability.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)


class WorkshopManager:
    """
    Manages multiple workshops with capacity and load balancing.
    """
    
    # Workshop database (in production, this would be in PostgreSQL)
    WORKSHOPS = {
        "WS-MUM-01": {
            "id": "WS-MUM-01",
            "name": "AutoCare Mumbai Central",
            "city": "Mumbai",
            "location": {"lat": 19.0760, "lon": 72.8777},
            "technician_capacity": 8,
            "bay_count": 6,
            "specializations": ["brake_system", "engine", "battery", "tyre"],
            "emergency_slots_per_day": 2,
            "operating_hours": {"start": "08:00", "end": "20:00"},
            "rating": 4.5,
            "parts_availability": {
                "brake_system": 0.95,
                "engine": 0.80,
                "battery": 0.90,
                "tyre": 0.85
            }
        },
        "WS-PUNE-01": {
            "id": "WS-PUNE-01",
            "name": "ServicePro Pune West",
            "city": "Pune",
            "location": {"lat": 18.5204, "lon": 73.8567},
            "technician_capacity": 6,
            "bay_count": 4,
            "specializations": ["brake_system", "engine", "battery"],
            "emergency_slots_per_day": 1,
            "operating_hours": {"start": "09:00", "end": "19:00"},
            "rating": 4.3,
            "parts_availability": {
                "brake_system": 0.90,
                "engine": 0.75,
                "battery": 0.95,
                "tyre": 0.70
            }
        },
        "WS-BLR-01": {
            "id": "WS-BLR-01",
            "name": "TechService Bangalore East",
            "city": "Bangalore",
            "location": {"lat": 12.9716, "lon": 77.5946},
            "technician_capacity": 10,
            "bay_count": 8,
            "specializations": ["brake_system", "engine", "battery", "tyre", "electrical"],
            "emergency_slots_per_day": 3,
            "operating_hours": {"start": "07:00", "end": "21:00"},
            "rating": 4.7,
            "parts_availability": {
                "brake_system": 0.98,
                "engine": 0.90,
                "battery": 0.95,
                "tyre": 0.92
            }
        },
        "WS-DEL-01": {
            "id": "WS-DEL-01",
            "name": "QuickFix Delhi South",
            "city": "Delhi",
            "location": {"lat": 28.7041, "lon": 77.1025},
            "technician_capacity": 7,
            "bay_count": 5,
            "specializations": ["brake_system", "engine", "battery", "tyre"],
            "emergency_slots_per_day": 2,
            "operating_hours": {"start": "08:00", "end": "20:00"},
            "rating": 4.4,
            "parts_availability": {
                "brake_system": 0.92,
                "engine": 0.85,
                "battery": 0.88,
                "tyre": 0.90
            }
        },
        "WS-CHE-01": {
            "id": "WS-CHE-01",
            "name": "AutoExpert Chennai North",
            "city": "Chennai",
            "location": {"lat": 13.0827, "lon": 80.2707},
            "technician_capacity": 9,
            "bay_count": 7,
            "specializations": ["brake_system", "engine", "battery", "tyre"],
            "emergency_slots_per_day": 2,
            "operating_hours": {"start": "08:00", "end": "20:00"},
            "rating": 4.6,
            "parts_availability": {
                "brake_system": 0.94,
                "engine": 0.88,
                "battery": 0.93,
                "tyre": 0.87
            }
        }
    }
    
    def __init__(self):
        """Initialize workshop manager."""
        # Current load tracking (in production, this would be in Redis)
        self.current_loads = {ws_id: 0.0 for ws_id in self.WORKSHOPS.keys()}
        self.emergency_slots_used = {ws_id: 0 for ws_id in self.WORKSHOPS.keys()}
        logger.info(f"Workshop Manager initialized with {len(self.WORKSHOPS)} workshops")
    
    def get_all_workshops(self) -> List[Dict[str, Any]]:
        """Get all workshops with current status."""
        workshops = []
        for ws_id, ws_data in self.WORKSHOPS.items():
            workshops.append({
                **ws_data,
                "current_load": self.current_loads[ws_id],
                "load_percentage": round(self.current_loads[ws_id] * 100, 1),
                "emergency_slots_available": ws_data["emergency_slots_per_day"] - self.emergency_slots_used[ws_id],
                "status": self._get_workshop_status(ws_id)
            })
        return workshops
    
    def get_workshop(self, workshop_id: str) -> Optional[Dict[str, Any]]:
        """Get specific workshop details."""
        if workshop_id not in self.WORKSHOPS:
            return None
        
        ws_data = self.WORKSHOPS[workshop_id]
        return {
            **ws_data,
            "current_load": self.current_loads[workshop_id],
            "load_percentage": round(self.current_loads[workshop_id] * 100, 1),
            "emergency_slots_available": ws_data["emergency_slots_per_day"] - self.emergency_slots_used[workshop_id],
            "status": self._get_workshop_status(workshop_id)
        }
    
    def find_best_workshop(
        self,
        component: str,
        risk_level: str,
        is_emergency: bool = False,
        preferred_city: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find the best workshop based on multiple criteria.
        
        Args:
            component: Component needing service
            risk_level: Risk level (low, medium, high)
            is_emergency: Whether this is an emergency
            preferred_city: Preferred city (optional)
        
        Returns:
            Best workshop with reasoning
        """
        candidates = []
        
        for ws_id, ws_data in self.WORKSHOPS.items():
            # Check if workshop handles this component
            if component not in ws_data["specializations"]:
                continue
            
            # Check parts availability
            parts_avail = ws_data["parts_availability"].get(component, 0)
            if parts_avail < 0.5:
                continue
            
            # Check emergency slot availability
            if is_emergency:
                emergency_avail = ws_data["emergency_slots_per_day"] - self.emergency_slots_used[ws_id]
                if emergency_avail <= 0:
                    continue
            
            # Calculate score
            score = 0.0
            
            # Load factor (lower is better)
            load_score = (1.0 - self.current_loads[ws_id]) * 30
            score += load_score
            
            # Parts availability
            parts_score = parts_avail * 25
            score += parts_score
            
            # Rating
            rating_score = (ws_data["rating"] / 5.0) * 20
            score += rating_score
            
            # Capacity
            capacity_score = (ws_data["technician_capacity"] / 10.0) * 15
            score += capacity_score
            
            # City preference
            if preferred_city and ws_data["city"].lower() == preferred_city.lower():
                score += 10
            
            candidates.append({
                "workshop_id": ws_id,
                "workshop_data": ws_data,
                "score": score,
                "load_score": load_score,
                "parts_score": parts_score,
                "rating_score": rating_score
            })
        
        if not candidates:
            # Fallback to any workshop
            ws_id = list(self.WORKSHOPS.keys())[0]
            return {
                "workshop_id": ws_id,
                "workshop_data": self.WORKSHOPS[ws_id],
                "score": 0,
                "reasoning": "Fallback: No optimal workshop found, using default"
            }
        
        # Sort by score
        candidates.sort(key=lambda x: x["score"], reverse=True)
        best = candidates[0]
        
        # Generate reasoning
        reasoning_parts = []
        if best["load_score"] > 20:
            reasoning_parts.append("low current load")
        if best["parts_score"] > 20:
            reasoning_parts.append("high parts availability")
        if best["rating_score"] > 15:
            reasoning_parts.append("excellent rating")
        
        reasoning = f"Selected based on: {', '.join(reasoning_parts)}"
        
        return {
            "workshop_id": best["workshop_id"],
            "workshop_data": best["workshop_data"],
            "score": best["score"],
            "reasoning": reasoning
        }
    
    def update_load(self, workshop_id: str, load_delta: float):
        """Update workshop load."""
        if workshop_id in self.current_loads:
            self.current_loads[workshop_id] = max(0.0, min(1.0, self.current_loads[workshop_id] + load_delta))
            logger.info(f"Updated load for {workshop_id}: {self.current_loads[workshop_id]:.2f}")
    
    def use_emergency_slot(self, workshop_id: str) -> bool:
        """Use an emergency slot."""
        if workshop_id not in self.WORKSHOPS:
            return False
        
        ws_data = self.WORKSHOPS[workshop_id]
        if self.emergency_slots_used[workshop_id] < ws_data["emergency_slots_per_day"]:
            self.emergency_slots_used[workshop_id] += 1
            logger.info(f"Used emergency slot at {workshop_id}: {self.emergency_slots_used[workshop_id]}/{ws_data['emergency_slots_per_day']}")
            return True
        
        return False
    
    def _get_workshop_status(self, workshop_id: str) -> str:
        """Get workshop status based on load."""
        load = self.current_loads[workshop_id]
        if load < 0.5:
            return "available"
        elif load < 0.8:
            return "busy"
        else:
            return "full"
    
    def reset_daily_counters(self):
        """Reset daily counters (emergency slots, etc.)."""
        self.emergency_slots_used = {ws_id: 0 for ws_id in self.WORKSHOPS.keys()}
        logger.info("Reset daily workshop counters")


# Global workshop manager instance
_workshop_manager = None


def get_workshop_manager() -> WorkshopManager:
    """Get singleton workshop manager instance."""
    global _workshop_manager
    if _workshop_manager is None:
        _workshop_manager = WorkshopManager()
    return _workshop_manager
