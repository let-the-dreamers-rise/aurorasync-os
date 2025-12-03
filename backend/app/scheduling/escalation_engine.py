"""
Escalation Engine for AuroraSync OS.
Handles critical failure escalation and emergency scheduling.
"""

from typing import Dict, Any, Optional, List
import logging


logger = logging.getLogger(__name__)


class EscalationEngine:
    """
    Evaluates failure severity and escalates critical cases.
    """
    
    # Critical thresholds
    CRITICAL_THRESHOLDS = {
        "brake_system": {
            "probability": 0.75,
            "timeframe_hours": 48
        },
        "engine": {
            "probability": 0.80,
            "timeframe_hours": 24
        },
        "battery": {
            "probability": 0.70,
            "timeframe_hours": 72
        },
        "tyre": {
            "probability": 0.65,
            "timeframe_hours": 48
        }
    }
    
    # Severity levels
    SEVERITY_LEVELS = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
        "EMERGENCY": 5
    }
    
    def __init__(self):
        """Initialize escalation engine."""
        self.escalation_count = 0
        logger.info("Escalation Engine initialized")
    
    def evaluate_escalation(
        self,
        risk_level: str,
        component: str,
        probability: float,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate if a case should be escalated.
        
        Args:
            risk_level: Risk level (low, medium, high)
            component: Component type
            probability: Failure probability (0.0 to 1.0)
            additional_context: Additional context (optional)
        
        Returns:
            Escalation decision with actions
        """
        # Get component thresholds
        thresholds = self.CRITICAL_THRESHOLDS.get(
            component,
            {"probability": 0.75, "timeframe_hours": 48}
        )
        
        # Determine severity
        severity = self._calculate_severity(
            risk_level,
            component,
            probability,
            thresholds
        )
        
        # Determine actions
        actions = self._determine_actions(severity, component, probability)
        
        # Check if escalation needed
        should_escalate = severity in ["CRITICAL", "EMERGENCY"]
        
        if should_escalate:
            self.escalation_count += 1
            logger.warning(
                f"ESCALATION #{self.escalation_count}: {component} - "
                f"Severity: {severity}, Probability: {probability:.2f}"
            )
        
        return {
            "severity": severity,
            "should_escalate": should_escalate,
            "actions": actions,
            "recommended_timeframe": self._get_timeframe(severity, thresholds),
            "override_preferences": severity == "EMERGENCY",
            "reasoning": self._generate_reasoning(severity, component, probability, thresholds),
            "escalation_id": f"ESC-{self.escalation_count:04d}" if should_escalate else None
        }
    
    def _calculate_severity(
        self,
        risk_level: str,
        component: str,
        probability: float,
        thresholds: Dict[str, Any]
    ) -> str:
        """Calculate severity level."""
        # Emergency conditions
        if component == "brake_system" and probability >= 0.90:
            return "EMERGENCY"
        if component == "engine" and probability >= 0.95:
            return "EMERGENCY"
        
        # Critical conditions
        if probability >= thresholds["probability"]:
            if risk_level == "high":
                return "CRITICAL"
            else:
                return "HIGH"
        
        # High conditions
        if probability >= 0.60:
            return "HIGH"
        
        # Medium conditions
        if probability >= 0.40:
            return "MEDIUM"
        
        # Low conditions
        return "LOW"
    
    def _determine_actions(
        self,
        severity: str,
        component: str,
        probability: float
    ) -> List[str]:
        """Determine required actions based on severity."""
        actions = []
        
        if severity == "EMERGENCY":
            actions.extend([
                "OVERRIDE_SCHEDULING",
                "FORCE_EARLIEST_SLOT",
                "SEND_URGENT_VOICE_ALERT",
                "NOTIFY_WORKSHOP_EMERGENCY",
                "RECOMMEND_TOW_SERVICE",
                "DISABLE_VEHICLE_IF_POSSIBLE"
            ])
        
        elif severity == "CRITICAL":
            actions.extend([
                "PRIORITIZE_SCHEDULING",
                "USE_EMERGENCY_SLOT",
                "SEND_URGENT_VOICE_ALERT",
                "NOTIFY_WORKSHOP_PRIORITY",
                "RECOMMEND_IMMEDIATE_SERVICE"
            ])
        
        elif severity == "HIGH":
            actions.extend([
                "EXPEDITE_SCHEDULING",
                "SEND_VOICE_ALERT",
                "RECOMMEND_EARLY_SERVICE"
            ])
        
        elif severity == "MEDIUM":
            actions.extend([
                "NORMAL_SCHEDULING",
                "SEND_VOICE_NOTIFICATION"
            ])
        
        else:  # LOW
            actions.extend([
                "NORMAL_SCHEDULING",
                "SEND_REMINDER"
            ])
        
        return actions
    
    def _get_timeframe(
        self,
        severity: str,
        thresholds: Dict[str, Any]
    ) -> str:
        """Get recommended timeframe."""
        if severity == "EMERGENCY":
            return "next 2 hours"
        elif severity == "CRITICAL":
            return "next 6 hours"
        elif severity == "HIGH":
            return f"next {thresholds['timeframe_hours']} hours"
        elif severity == "MEDIUM":
            return "next 3-7 days"
        else:
            return "next 1-2 weeks"
    
    def _generate_reasoning(
        self,
        severity: str,
        component: str,
        probability: float,
        thresholds: Dict[str, Any]
    ) -> str:
        """Generate human-readable reasoning."""
        if severity == "EMERGENCY":
            return (
                f"EMERGENCY: {component} failure probability {probability:.0%} "
                f"exceeds critical threshold. Immediate action required to prevent "
                f"safety hazard or complete breakdown."
            )
        
        elif severity == "CRITICAL":
            return (
                f"CRITICAL: {component} failure probability {probability:.0%} "
                f"is above threshold ({thresholds['probability']:.0%}). "
                f"Urgent service required within {thresholds['timeframe_hours']} hours."
            )
        
        elif severity == "HIGH":
            return (
                f"HIGH: {component} showing significant failure risk ({probability:.0%}). "
                f"Early service recommended to prevent escalation."
            )
        
        elif severity == "MEDIUM":
            return (
                f"MEDIUM: {component} showing moderate failure risk ({probability:.0%}). "
                f"Schedule service at your convenience within the week."
            )
        
        else:
            return (
                f"LOW: {component} showing minor wear ({probability:.0%}). "
                f"Routine maintenance recommended."
            )
    
    def check_safety_to_drive(
        self,
        component: str,
        probability: float,
        severity: str
    ) -> Dict[str, Any]:
        """
        Check if it's safe to drive.
        
        Args:
            component: Component type
            probability: Failure probability
            severity: Severity level
        
        Returns:
            Safety assessment
        """
        if severity == "EMERGENCY":
            return {
                "safe_to_drive": False,
                "recommendation": "DO NOT DRIVE",
                "reason": f"{component} failure imminent. Arrange tow service immediately.",
                "max_distance_km": 0
            }
        
        elif severity == "CRITICAL":
            return {
                "safe_to_drive": "limited",
                "recommendation": "DRIVE TO SERVICE CENTER ONLY",
                "reason": f"{component} at high risk. Avoid highways and long distances.",
                "max_distance_km": 10
            }
        
        elif severity == "HIGH":
            return {
                "safe_to_drive": "with_caution",
                "recommendation": "DRIVE WITH CAUTION",
                "reason": f"{component} showing significant wear. Avoid aggressive driving.",
                "max_distance_km": 50
            }
        
        else:
            return {
                "safe_to_drive": True,
                "recommendation": "SAFE TO DRIVE",
                "reason": f"{component} condition acceptable. Schedule service soon.",
                "max_distance_km": None
            }


# Global escalation engine instance
_escalation_engine = None


def get_escalation_engine() -> EscalationEngine:
    """Get singleton escalation engine instance."""
    global _escalation_engine
    if _escalation_engine is None:
        _escalation_engine = EscalationEngine()
    return _escalation_engine
