"""
UEBA Event model for security monitoring and anomaly detection.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class UEBAEvent(Base):
    """
    UEBA (User and Entity Behavior Analytics) Event table.
    Stores security events and anomaly detection results for agent monitoring.
    
    Attributes:
        id: Primary key (auto-increment)
        event_id: Unique event identifier (e.g., UEBA-9999)
        agent_name: Name of the agent being monitored
        action: Action performed by the agent
        resource: Resource accessed (e.g., API endpoint, database table)
        metric: Metric being monitored (e.g., response_time, request_rate)
        baseline: Normal baseline value for the metric
        observed: Observed value that triggered the event
        anomaly_score: Anomaly score (0.0 to 1.0, higher = more anomalous)
        severity: Event severity (low, medium, high, critical)
        action_taken: Action taken in response (e.g., alert_admin, throttle, restart)
        metadata: Additional event metadata (JSON)
        timestamp: When the event occurred
    """
    
    __tablename__ = "ueba_events"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Event identification
    event_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Agent information
    agent_name = Column(
        String(50),
        nullable=False,
        index=True,
        comment="Name of the agent: master, data_analysis, diagnosis, etc."
    )
    action = Column(
        String(100),
        nullable=False,
        comment="Action performed: process_data, predict_failure, etc."
    )
    resource = Column(
        String(200),
        nullable=True,
        comment="Resource accessed: API endpoint, database table, etc."
    )
    
    # Metrics
    metric = Column(
        String(50),
        nullable=False,
        comment="Metric monitored: response_time, request_rate, error_rate, etc."
    )
    baseline = Column(
        Float,
        nullable=True,
        comment="Normal baseline value for the metric"
    )
    observed = Column(
        Float,
        nullable=False,
        comment="Observed value that triggered the event"
    )
    anomaly_score = Column(
        Float,
        nullable=False,
        comment="Anomaly score (0.0 to 1.0, higher = more anomalous)"
    )
    
    # Severity and response
    severity = Column(
        String(20),
        nullable=False,
        comment="Event severity: low, medium, high, critical"
    )
    action_taken = Column(
        String(100),
        nullable=True,
        comment="Action taken: alert_admin, throttle, restart, none"
    )
    
    # Additional information
    description = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True, comment="Additional event metadata")
    
    # Timestamp
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    def __repr__(self):
        return (
            f"<UEBAEvent(event_id='{self.event_id}', "
            f"agent='{self.agent_name}', "
            f"severity='{self.severity}', "
            f"anomaly_score={self.anomaly_score:.2f})>"
        )
