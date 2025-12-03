"""
Prediction API routes for AuroraSync OS.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

router = APIRouter()


@router.get("/mock", tags=["Predictions"])
def get_mock_predictions() -> Dict[str, Any]:
    """
    Get mock predictions for demo purposes.
    
    Returns a set of sample predictions without requiring input.
    Perfect for frontend demos and testing!
    
    Returns:
        Dictionary with mock prediction data
    """
    return {
        "status": "success",
        "predictions": [
            {
                "vehicle_id": "VEH001",
                "owner": "Rahul Kumar",
                "model": "Honda Accord",
                "prediction": {
                    "failure_risk": "HIGH",
                    "probability": 0.85,
                    "component": "brake_system",
                    "confidence": 0.92,
                    "days_until_failure": 7,
                    "recommended_action": "Schedule immediate service"
                }
            },
            {
                "vehicle_id": "VEH002",
                "owner": "Priya Sharma",
                "model": "Toyota Camry",
                "prediction": {
                    "failure_risk": "MEDIUM",
                    "probability": 0.42,
                    "component": "electrical_system",
                    "confidence": 0.88,
                    "days_until_failure": 30,
                    "recommended_action": "Schedule service within 2 weeks"
                }
            },
            {
                "vehicle_id": "VEH003",
                "owner": "Amit Patel",
                "model": "Maruti Swift",
                "prediction": {
                    "failure_risk": "LOW",
                    "probability": 0.12,
                    "component": "none",
                    "confidence": 0.95,
                    "days_until_failure": 90,
                    "recommended_action": "Continue normal operation"
                }
            },
            {
                "vehicle_id": "VEH004",
                "owner": "Sneha Reddy",
                "model": "Hyundai Creta",
                "prediction": {
                    "failure_risk": "HIGH",
                    "probability": 0.78,
                    "component": "cooling_system",
                    "confidence": 0.90,
                    "days_until_failure": 10,
                    "recommended_action": "Schedule immediate service"
                }
            },
            {
                "vehicle_id": "VEH005",
                "owner": "Vikram Singh",
                "model": "Mahindra XUV500",
                "prediction": {
                    "failure_risk": "MEDIUM",
                    "probability": 0.38,
                    "component": "suspension",
                    "confidence": 0.87,
                    "days_until_failure": 45,
                    "recommended_action": "Schedule service within 2 weeks"
                }
            }
        ],
        "summary": {
            "total_vehicles": 5,
            "high_risk": 2,
            "medium_risk": 2,
            "low_risk": 1,
            "avg_probability": 0.51
        }
    }


class TelematicsInput(BaseModel):
    """
    Input model for telematics data.
    """
    engine_temp: float = Field(..., description="Engine temperature in °C", ge=0, le=150)
    brake_pad_wear: float = Field(..., description="Brake pad wear in mm", ge=0, le=15)
    battery_voltage: float = Field(..., description="Battery voltage in V", ge=10, le=15)
    vibration: float = Field(..., description="Vibration level (0-2 scale)", ge=0, le=2)
    tyre_pressure: float = Field(..., description="Tyre pressure in PSI", ge=15, le=50)
    odometer: float = Field(..., description="Odometer reading in km", ge=0)
    ambient_temp: float = Field(..., description="Ambient temperature in °C", ge=-20, le=60)
    
    class Config:
        json_schema_extra = {
            "example": {
                "engine_temp": 110.0,
                "brake_pad_wear": 2.0,
                "battery_voltage": 11.5,
                "vibration": 1.2,
                "tyre_pressure": 28.0,
                "odometer": 50000.0,
                "ambient_temp": 35.0
            }
        }


class PredictionResponse(BaseModel):
    """
    Response model for predictions.
    """
    status: str
    input: Dict[str, float]
    prediction: Dict[str, Any]


@router.post("/test", response_model=PredictionResponse, tags=["Predictions"])
def test_prediction(telematics: TelematicsInput) -> Dict[str, Any]:
    """
    Test failure prediction endpoint.
    
    Returns mock predictions for demo purposes - no ML model required!
    
    **Risk Levels:**
    - **LOW**: Probability < 0.2 (< 20%)
    - **MEDIUM**: 0.2 ≤ Probability < 0.5 (20-50%)
    - **HIGH**: Probability ≥ 0.5 (≥ 50%)
    
    **Example Request:**
    ```json
    {
        "engine_temp": 110.0,
        "brake_pad_wear": 2.0,
        "battery_voltage": 11.5,
        "vibration": 1.2,
        "tyre_pressure": 28.0,
        "odometer": 50000.0,
        "ambient_temp": 35.0
    }
    ```
    
    **Example Response:**
    ```json
    {
        "status": "success",
        "input": { ... },
        "prediction": {
            "failure_risk": "HIGH",
            "probability": 0.8542,
            "component": "brake_system",
            "confidence": 0.92
        }
    }
    ```
    
    Args:
        telematics: Telematics input data
    
    Returns:
        Prediction response with risk level and probability
    """
    # Convert input to dictionary
    features = telematics.model_dump()
    
    # Generate mock prediction based on input values
    # This creates realistic-looking predictions for demo
    
    # Determine risk based on critical values
    high_risk = (
        features["engine_temp"] > 105 or
        features["brake_pad_wear"] < 4 or
        features["battery_voltage"] < 12.0 or
        features["vibration"] > 1.3
    )
    
    medium_risk = (
        features["engine_temp"] > 95 or
        features["brake_pad_wear"] < 6 or
        features["battery_voltage"] < 12.4 or
        features["vibration"] > 0.8
    )
    
    # Determine component at risk
    if features["brake_pad_wear"] < 5:
        component = "brake_system"
        probability = 0.85
    elif features["battery_voltage"] < 12.0:
        component = "electrical_system"
        probability = 0.78
    elif features["engine_temp"] > 105:
        component = "cooling_system"
        probability = 0.82
    elif features["vibration"] > 1.3:
        component = "suspension"
        probability = 0.73
    elif medium_risk:
        component = "general_wear"
        probability = 0.42
    else:
        component = "none"
        probability = 0.12
    
    # Determine risk level
    if high_risk:
        risk_level = "HIGH"
    elif medium_risk:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    # Build prediction response
    prediction = {
        "failure_risk": risk_level,
        "probability": round(probability, 4),
        "component": component,
        "confidence": 0.92,
        "days_until_failure": 7 if high_risk else (30 if medium_risk else 90),
        "recommended_action": (
            "Schedule immediate service" if high_risk else
            "Schedule service within 2 weeks" if medium_risk else
            "Continue normal operation"
        ),
        "thresholds": {
            "low": 0.2,
            "medium": 0.5
        }
    }
    
    # Return response
    return {
        "status": "success",
        "input": features,
        "prediction": prediction
    }


@router.get("/model-info", tags=["Predictions"])
def model_info() -> Dict[str, Any]:
    """
    Get information about the prediction system.
    
    Returns mock model info for demo - no ML model required!
    
    Returns:
        Dictionary with model information including:
        - Model type
        - Features used
        - Risk thresholds
        - Status
    """
    return {
        "model_type": "MockPredictor",
        "description": "Demo prediction system - no ML dependencies required",
        "version": "1.0.0",
        "features": [
            "engine_temp",
            "brake_pad_wear",
            "battery_voltage",
            "vibration",
            "tyre_pressure",
            "odometer",
            "ambient_temp"
        ],
        "n_features": 7,
        "risk_thresholds": {
            "low": 0.2,
            "medium": 0.5
        },
        "components_detected": [
            "brake_system",
            "electrical_system",
            "cooling_system",
            "suspension",
            "general_wear"
        ],
        "is_loaded": True,
        "requires_training": False,
        "accuracy": 0.92,
        "last_updated": "2024-12-03"
    }


@router.post("/batch", tags=["Predictions"])
def batch_prediction(telematics_list: list[TelematicsInput]) -> Dict[str, Any]:
    """
    Batch prediction endpoint for multiple vehicles.
    
    Returns mock predictions for demo - no ML model required!
    
    Args:
        telematics_list: List of telematics input data
    
    Returns:
        Dictionary with batch prediction results
    """
    predictions = []
    
    for idx, telematics in enumerate(telematics_list):
        # Reuse the test_prediction logic
        result = test_prediction(telematics)
        
        predictions.append({
            "index": idx,
            "vehicle_id": f"VEH{str(idx+1).zfill(3)}",
            "input": result["input"],
            "prediction": result["prediction"]
        })
    
    return {
        "status": "success",
        "count": len(predictions),
        "predictions": predictions,
        "summary": {
            "high_risk": sum(1 for p in predictions if p["prediction"]["failure_risk"] == "HIGH"),
            "medium_risk": sum(1 for p in predictions if p["prediction"]["failure_risk"] == "MEDIUM"),
            "low_risk": sum(1 for p in predictions if p["prediction"]["failure_risk"] == "LOW")
        }
    }
