"""
Scheduling API routes for AuroraSync OS.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.scheduling.scheduler import get_scheduler
from app.scheduling.workshop_manager import get_workshop_manager
from app.scheduling.demand_forecaster import get_demand_forecaster
from app.scheduling.slot_manager import get_slot_manager
from app.scheduling.rca_insights import get_rca_insights


router = APIRouter()


class ScheduleRequest(BaseModel):
    """Request model for scheduling."""
    vehicle_id: str = Field(..., description="Vehicle ID")
    component: str = Field(..., description="Component needing service")
    risk_level: str = Field(..., description="Risk level (low, medium, high)")
    probability: float = Field(..., description="Failure probability (0.0 to 1.0)")
    owner_preferences: Optional[Dict[str, Any]] = Field(None, description="Owner preferences")
    vehicle_location: Optional[str] = Field(None, description="Vehicle location/city")
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_id": "VEH001",
                "component": "brake_system",
                "risk_level": "high",
                "probability": 0.82,
                "owner_preferences": {
                    "preferred_time": "afternoon",
                    "preferred_day": "tomorrow",
                    "preferred_city": "Mumbai"
                },
                "vehicle_location": "Mumbai"
            }
        }


@router.post("/auto", tags=["Scheduling"])
def auto_schedule(request: ScheduleRequest) -> Dict[str, Any]:
    """
    Autonomous intelligent scheduling.
    
    This endpoint orchestrates the complete scheduling process:
    - Evaluates failure severity and escalation
    - Selects optimal workshop with load balancing
    - Forecasts demand and finds best slot
    - Honors owner preferences (unless emergency override)
    - Books appointment automatically
    
    Args:
        request: Scheduling request
    
    Returns:
        Complete scheduling result with workshop, slot, and reasoning
    
    Raises:
        HTTPException: If scheduling fails
    """
    try:
        scheduler = get_scheduler()
        
        result = scheduler.schedule_appointment(
            vehicle_id=request.vehicle_id,
            component=request.component,
            risk_level=request.risk_level,
            probability=request.probability,
            owner_preferences=request.owner_preferences,
            vehicle_location=request.vehicle_location
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scheduling failed: {str(e)}"
        )


@router.get("/workshops", tags=["Scheduling"])
def get_workshops() -> Dict[str, Any]:
    """
    Get all workshops with current status.
    
    Returns:
        List of workshops with load, capacity, and availability
    """
    try:
        workshop_manager = get_workshop_manager()
        workshops = workshop_manager.get_all_workshops()
        
        return {
            "status": "success",
            "count": len(workshops),
            "workshops": workshops
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get workshops: {str(e)}"
        )


@router.get("/workshops/{workshop_id}", tags=["Scheduling"])
def get_workshop(workshop_id: str) -> Dict[str, Any]:
    """
    Get specific workshop details.
    
    Args:
        workshop_id: Workshop ID
    
    Returns:
        Workshop details
    
    Raises:
        HTTPException: If workshop not found
    """
    try:
        workshop_manager = get_workshop_manager()
        workshop = workshop_manager.get_workshop(workshop_id)
        
        if not workshop:
            raise HTTPException(
                status_code=404,
                detail=f"Workshop not found: {workshop_id}"
            )
        
        return {
            "status": "success",
            "workshop": workshop
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get workshop: {str(e)}"
        )


@router.get("/forecast/{workshop_id}", tags=["Scheduling"])
def get_demand_forecast(workshop_id: str, days: int = 7) -> Dict[str, Any]:
    """
    Get demand forecast for a workshop.
    
    Args:
        workshop_id: Workshop ID
        days: Number of days to forecast
    
    Returns:
        Demand forecast with load curve
    """
    try:
        demand_forecaster = get_demand_forecaster()
        
        forecast = demand_forecaster.forecast_demand(workshop_id, days)
        load_curve = demand_forecaster.get_workshop_load_curve(workshop_id, days)
        
        return {
            "status": "success",
            "workshop_id": workshop_id,
            "forecast": forecast,
            "load_curve": load_curve
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get forecast: {str(e)}"
        )


@router.get("/slots/{workshop_id}", tags=["Scheduling"])
def get_available_slots(workshop_id: str, days: int = 7) -> Dict[str, Any]:
    """
    Get available slots for a workshop.
    
    Args:
        workshop_id: Workshop ID
        days: Number of days to generate slots
    
    Returns:
        Available slots
    """
    try:
        workshop_manager = get_workshop_manager()
        slot_manager = get_slot_manager()
        
        workshop = workshop_manager.get_workshop(workshop_id)
        if not workshop:
            raise HTTPException(
                status_code=404,
                detail=f"Workshop not found: {workshop_id}"
            )
        
        from datetime import datetime
        slots = slot_manager.generate_slots(
            workshop_id,
            workshop,
            datetime.now(),
            days,
            include_emergency=True
        )
        
        return {
            "status": "success",
            "workshop_id": workshop_id,
            "total_slots": len(slots),
            "slots": slots
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get slots: {str(e)}"
        )


@router.post("/insights/rca", tags=["Scheduling", "Insights"])
def generate_rca_report(
    component: Optional[str] = None,
    days: int = 30
) -> Dict[str, Any]:
    """
    Generate RCA (Root Cause Analysis) report.
    
    Analyzes failure patterns and generates manufacturing insights.
    
    Args:
        component: Specific component to analyze (optional)
        days: Days to analyze
    
    Returns:
        RCA report with recommendations
    """
    try:
        rca_insights = get_rca_insights()
        
        report = rca_insights.generate_rca_report(component, days)
        validation = rca_insights.validate_predictions()
        
        return {
            "status": "success",
            "rca_report": report,
            "prediction_validation": validation
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate RCA report: {str(e)}"
        )


@router.get("/analytics/overview", tags=["Scheduling", "Analytics"])
def get_scheduling_analytics() -> Dict[str, Any]:
    """
    Get scheduling system analytics overview.
    
    Returns:
        System-wide analytics and metrics
    """
    try:
        scheduler = get_scheduler()
        workshop_manager = get_workshop_manager()
        
        workshops = workshop_manager.get_all_workshops()
        
        # Calculate metrics
        total_capacity = sum(w["technician_capacity"] for w in workshops)
        avg_load = sum(w["current_load"] for w in workshops) / len(workshops)
        
        return {
            "status": "success",
            "analytics": {
                "total_bookings": scheduler.booking_count,
                "total_workshops": len(workshops),
                "total_capacity": total_capacity,
                "average_load": round(avg_load, 2),
                "workshops_by_status": {
                    "available": len([w for w in workshops if w["status"] == "available"]),
                    "busy": len([w for w in workshops if w["status"] == "busy"]),
                    "full": len([w for w in workshops if w["status"] == "full"])
                }
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get analytics: {str(e)}"
        )
