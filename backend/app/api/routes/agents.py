"""
Agent API routes for testing and monitoring.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

from app.agents import get_master_agent


router = APIRouter()


class EventRequest(BaseModel):
    """
    Request model for agent event routing.
    """
    type: str = Field(..., description="Event type (e.g., 'predict_failure', 'analyze_data')")
    payload: Optional[Dict[str, Any]] = Field(default={}, description="Event payload data")
    source: Optional[str] = Field(default="api", description="Event source")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "predict_failure",
                "payload": {
                    "vehicle_id": "VEH001",
                    "features": {
                        "rpm_avg": 2500,
                        "temp_avg": 85.5
                    }
                },
                "source": "api"
            }
        }


class EventResponse(BaseModel):
    """
    Response model for agent events.
    """
    status: str
    agent: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


@router.post("/test-route", response_model=EventResponse, tags=["Agents"])
def test_agent_routing(event: EventRequest) -> Dict[str, Any]:
    """
    Test agent routing by sending an event to the Master Agent.
    
    This endpoint allows you to test the multi-agent system by sending
    events and seeing how they are routed to the appropriate worker agents.
    
    The Master Agent will:
    1. Log the event with UEBA
    2. Route to the appropriate worker agent
    3. Return the agent's response
    
    **Available Event Types:**
    
    **Data Analysis Agent:**
    - `analyze_data` - Analyze raw telematics data
    - `extract_features` - Extract features from data
    - `detect_anomaly` - Detect anomalies in data
    
    **Diagnosis Agent:**
    - `predict_failure` - Predict vehicle failure
    - `diagnose_issue` - Diagnose a specific issue
    - `assess_risk` - Assess risk level
    
    **Customer Engagement Agent:**
    - `engage_customer` - Engage with customer
    - `generate_call_script` - Generate call script
    - `send_notification` - Send notification
    
    **Scheduling Agent:**
    - `schedule_service` - Schedule a service appointment
    - `find_availability` - Find available slots
    - `book_appointment` - Book an appointment
    
    **Feedback Agent:**
    - `validate_prediction` - Validate a prediction
    - `collect_feedback` - Collect service feedback
    - `calculate_accuracy` - Calculate model accuracy
    
    **Manufacturing Insights Agent:**
    - `generate_rca` - Generate RCA report
    - `create_capa` - Create CAPA report
    - `analyze_patterns` - Analyze failure patterns
    
    **UEBA Agent:**
    - `get_ueba_stats` - Get UEBA statistics
    
    Args:
        event: Event to route
    
    Returns:
        Response from the agent that processed the event
    
    Raises:
        HTTPException: If routing fails
    """
    try:
        # Get Master Agent singleton
        master_agent = get_master_agent()
        
        # Create event dictionary
        event_dict = {
            "type": event.type,
            "payload": event.payload,
            "source": event.source,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Route event through Master Agent
        response = master_agent.route_event(event_dict)
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent routing failed: {str(e)}"
        )


@router.get("/status", tags=["Agents"])
def get_agent_status() -> Dict[str, Any]:
    """
    Get status of all agents in the system.
    
    Returns information about:
    - Master Agent status
    - Worker agent availability
    - Event routing configuration
    - UEBA statistics
    
    Returns:
        Dictionary with agent status information
    """
    try:
        master_agent = get_master_agent()
        return master_agent.get_agent_status()
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get agent status: {str(e)}"
        )


@router.get("/ueba/stats", tags=["Agents", "UEBA"])
def get_ueba_statistics() -> Dict[str, Any]:
    """
    Get UEBA (User and Entity Behavior Analytics) statistics.
    
    Returns:
        Dictionary with UEBA statistics including:
        - Total actions logged
        - Monitoring status
        - Anomalies detected
        - Agents monitored
    """
    try:
        master_agent = get_master_agent()
        return master_agent.ueba_agent.get_statistics()
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get UEBA statistics: {str(e)}"
        )


@router.get("/event-types", tags=["Agents"])
def get_available_event_types() -> Dict[str, Any]:
    """
    Get list of all available event types and their routing.
    
    Returns:
        Dictionary mapping event types to their target agents
    """
    return {
        "data_analysis": [
            "analyze_data",
            "extract_features",
            "detect_anomaly"
        ],
        "diagnosis": [
            "predict_failure",
            "diagnose_issue",
            "assess_risk"
        ],
        "customer_engagement": [
            "engage_customer",
            "generate_call_script",
            "send_notification"
        ],
        "scheduling": [
            "schedule_service",
            "find_availability",
            "book_appointment"
        ],
        "feedback": [
            "validate_prediction",
            "collect_feedback",
            "calculate_accuracy"
        ],
        "manufacturing_insights": [
            "generate_rca",
            "create_capa",
            "analyze_patterns"
        ],
        "ueba": [
            "get_ueba_stats",
            "check_anomaly"
        ]
    }
