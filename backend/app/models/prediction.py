"""
Prediction model for storing ML-based failure predictions.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Prediction(Base):
    """
    Prediction table stores ML model predictions for vehicle failures.
    
    Attributes:
        id: Primary key (auto-increment)
        prediction_id: Unique prediction identifier (e.g., PRED-12345)
        vehicle_id: Foreign key to vehicles table
        component: Component at risk (e.g., brake_system, cooling_system)
        failure_probability: Probability of failure (0.0 to 1.0)
        severity: Severity level (low, medium, high, critical)
        predicted_failure_date: Estimated date of failure
        confidence: Model confidence score (0.0 to 1.0)
        model_version: Version of ML model used
        recommended_action: Suggested action (e.g., immediate_service, schedule_maintenance)
        created_at: Timestamp when prediction was made
    """
    
    __tablename__ = "predictions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Prediction identification
    prediction_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Vehicle reference
    vehicle_id = Column(String(20), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    
    # Prediction details
    component = Column(
        String(50),
        nullable=False,
        comment="Component at risk: brake_system, cooling_system, electrical_system, etc."
    )
    failure_probability = Column(
        Float,
        nullable=False,
        comment="Probability of failure (0.0 to 1.0)"
    )
    severity = Column(
        String(20),
        nullable=False,
        comment="Severity level: low, medium, high, critical"
    )
    predicted_failure_date = Column(
        Date,
        nullable=True,
        comment="Estimated date when failure will occur"
    )
    
    # Model metadata
    confidence = Column(
        Float,
        default=0.0,
        comment="Model confidence score (0.0 to 1.0)"
    )
    model_version = Column(String(20), default="v1.0.0")
    
    # Recommended action
    recommended_action = Column(
        String(50),
        nullable=True,
        comment="Suggested action: immediate_service, schedule_maintenance, monitor"
    )
    
    # Additional details
    notes = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return (
            f"<Prediction(prediction_id='{self.prediction_id}', "
            f"vehicle_id='{self.vehicle_id}', "
            f"component='{self.component}', "
            f"probability={self.failure_probability:.2f})>"
        )
