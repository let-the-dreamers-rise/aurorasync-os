"""
Failure Prediction Module for AuroraSync OS.

Lightweight rule-based predictor that works without scikit-learn.
Uses intelligent heuristics to predict vehicle failures.
"""

from typing import Dict, Any
import logging
import math


logger = logging.getLogger(__name__)

# Feature columns
FEATURE_COLUMNS = [
    "engine_temp",
    "brake_pad_wear",
    "battery_voltage",
    "vibration",
    "tyre_pressure",
    "odometer",
    "ambient_temp"
]

# Risk thresholds
RISK_THRESHOLDS = {
    "low": 0.2,
    "medium": 0.5
}

# Feature risk weights and thresholds
FEATURE_WEIGHTS = {
    "engine_temp": {"weight": 0.20, "critical": 110, "warning": 100, "optimal": 90},
    "brake_pad_wear": {"weight": 0.25, "critical": 3, "warning": 5, "optimal": 8},
    "battery_voltage": {"weight": 0.15, "critical": 11.5, "warning": 12.0, "optimal": 12.6},
    "vibration": {"weight": 0.15, "critical": 1.5, "warning": 1.0, "optimal": 0.5},
    "tyre_pressure": {"weight": 0.10, "critical": 25, "warning": 28, "optimal": 32},
    "odometer": {"weight": 0.10, "critical": 100000, "warning": 75000, "optimal": 50000},
    "ambient_temp": {"weight": 0.05, "critical": 45, "warning": 35, "optimal": 25}
}


def calculate_feature_risk(feature_name: str, value: float) -> float:
    """
    Calculate risk score for a single feature (0.0 to 1.0).
    
    Args:
        feature_name: Name of the feature
        value: Feature value
    
    Returns:
        Risk score between 0.0 (optimal) and 1.0 (critical)
    """
    config = FEATURE_WEIGHTS[feature_name]
    
    # Handle different risk directions
    if feature_name in ["battery_voltage", "tyre_pressure"]:
        # Lower is worse
        if value <= config["critical"]:
            return 1.0
        elif value <= config["warning"]:
            return 0.6 + 0.4 * (config["warning"] - value) / (config["warning"] - config["critical"])
        elif value <= config["optimal"]:
            return 0.3 * (config["optimal"] - value) / (config["optimal"] - config["warning"])
        else:
            return 0.0
    
    elif feature_name == "brake_pad_wear":
        # Lower is worse (wear means less pad remaining)
        if value <= config["critical"]:
            return 1.0
        elif value <= config["warning"]:
            return 0.6 + 0.4 * (config["warning"] - value) / (config["warning"] - config["critical"])
        elif value <= config["optimal"]:
            return 0.3 * (config["optimal"] - value) / (config["optimal"] - config["warning"])
        else:
            return 0.0
    
    else:
        # Higher is worse (engine_temp, vibration, odometer, ambient_temp)
        if value >= config["critical"]:
            return 1.0
        elif value >= config["warning"]:
            return 0.6 + 0.4 * (value - config["warning"]) / (config["critical"] - config["warning"])
        elif value >= config["optimal"]:
            return 0.3 * (value - config["optimal"]) / (config["warning"] - config["optimal"])
        else:
            return 0.0


def load_model() -> str:
    """
    Mock model loading for compatibility.
    
    Returns:
        Model type string
    """
    logger.info("Using lightweight rule-based predictor (no ML dependencies required)")
    return "RuleBasedPredictor"


def validate_features(features: Dict[str, Any]) -> None:
    """
    Validate that all required features are present.
    
    Args:
        features: Dictionary of feature values
    
    Raises:
        ValueError: If required features are missing or invalid
    """
    # Check for missing features
    missing_features = [col for col in FEATURE_COLUMNS if col not in features]
    if missing_features:
        raise ValueError(
            f"Missing required features: {', '.join(missing_features)}. "
            f"Required features: {', '.join(FEATURE_COLUMNS)}"
        )
    
    # Check for None values
    none_features = [col for col in FEATURE_COLUMNS if features[col] is None]
    if none_features:
        raise ValueError(
            f"Features cannot be None: {', '.join(none_features)}"
        )
    
    # Validate data types (should be numeric)
    for col in FEATURE_COLUMNS:
        try:
            float(features[col])
        except (TypeError, ValueError):
            raise ValueError(
                f"Feature '{col}' must be numeric, got: {type(features[col]).__name__}"
            )


def calculate_risk_level(probability: float) -> str:
    """
    Calculate risk level based on failure probability.
    
    Args:
        probability: Failure probability (0.0 to 1.0)
    
    Returns:
        Risk level: "LOW", "MEDIUM", or "HIGH"
    """
    if probability < RISK_THRESHOLDS["low"]:
        return "LOW"
    elif probability < RISK_THRESHOLDS["medium"]:
        return "MEDIUM"
    else:
        return "HIGH"


def predict_failure(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict vehicle failure based on telematics features.
    
    Uses intelligent rule-based heuristics to calculate failure probability
    based on weighted feature risks.
    
    Args:
        features: Dictionary with the following keys:
            - engine_temp: Engine temperature (°C)
            - brake_pad_wear: Brake pad wear (mm)
            - battery_voltage: Battery voltage (V)
            - vibration: Vibration level (0-2 scale)
            - tyre_pressure: Tyre pressure (PSI)
            - odometer: Odometer reading (km)
            - ambient_temp: Ambient temperature (°C)
    
    Returns:
        Dictionary with prediction results:
            - failure_risk: Risk level ("LOW", "MEDIUM", "HIGH")
            - probability: Failure probability (0.0 to 1.0)
            - thresholds: Risk thresholds used
            - features_used: Features used for prediction
            - feature_contributions: Individual feature risk scores
    
    Raises:
        ValueError: If features are invalid
    
    Example:
        >>> features = {
        ...     "engine_temp": 110.0,
        ...     "brake_pad_wear": 2.0,
        ...     "battery_voltage": 11.5,
        ...     "vibration": 1.2,
        ...     "tyre_pressure": 28.0,
        ...     "odometer": 50000.0,
        ...     "ambient_temp": 35.0
        ... }
        >>> result = predict_failure(features)
        >>> print(result["failure_risk"])
        HIGH
    """
    # Validate features
    validate_features(features)
    
    # Load model (just logs info)
    load_model()
    
    # Calculate weighted risk score
    total_risk = 0.0
    feature_contributions = {}
    
    for feature_name in FEATURE_COLUMNS:
        feature_value = features[feature_name]
        feature_risk = calculate_feature_risk(feature_name, feature_value)
        weight = FEATURE_WEIGHTS[feature_name]["weight"]
        
        weighted_risk = feature_risk * weight
        total_risk += weighted_risk
        
        feature_contributions[feature_name] = {
            "value": feature_value,
            "risk_score": round(feature_risk, 4),
            "weighted_contribution": round(weighted_risk, 4)
        }
    
    # Add some non-linearity to make it more realistic
    # High risks compound exponentially
    if total_risk > 0.5:
        total_risk = 0.5 + (total_risk - 0.5) * 1.3
    
    # Add small random variation for realism (±2%)
    import random
    random.seed(int(sum(features.values()) * 1000))
    variation = random.uniform(-0.02, 0.02)
    probability = max(0.0, min(1.0, total_risk + variation))
    
    # Calculate risk level
    risk_level = calculate_risk_level(probability)
    
    # Return results
    return {
        "failure_risk": risk_level,
        "probability": round(probability, 4),
        "thresholds": RISK_THRESHOLDS,
        "features_used": FEATURE_COLUMNS,
        "feature_contributions": feature_contributions,
        "model_type": "RuleBasedPredictor"
    }


def get_model_info() -> Dict[str, Any]:
    """
    Get information about the predictor.
    
    Returns:
        Dictionary with model information
    """
    return {
        "model_type": "RuleBasedPredictor",
        "description": "Lightweight rule-based failure predictor (no ML dependencies)",
        "features": FEATURE_COLUMNS,
        "n_features": len(FEATURE_COLUMNS),
        "risk_thresholds": RISK_THRESHOLDS,
        "feature_weights": {k: v["weight"] for k, v in FEATURE_WEIGHTS.items()},
        "is_loaded": True,
        "requires_training": False
    }
