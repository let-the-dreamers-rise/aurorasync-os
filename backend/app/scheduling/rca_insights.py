"""
RCA (Root Cause Analysis) Insights for AuroraSync OS.
Analyzes failure patterns and generates manufacturing feedback.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from collections import Counter


logger = logging.getLogger(__name__)


class RCAInsights:
    """
    Generates RCA/CAPA insights from failure patterns.
    """
    
    def __init__(self):
        """Initialize RCA insights."""
        # Mock failure history (in production, from database)
        self.failure_history: List[Dict[str, Any]] = []
        self.prediction_history: List[Dict[str, Any]] = []
        logger.info("RCA Insights initialized")
    
    def log_prediction(
        self,
        vehicle_id: str,
        component: str,
        probability: float,
        predicted_date: str
    ):
        """Log a prediction for later validation."""
        self.prediction_history.append({
            "vehicle_id": vehicle_id,
            "component": component,
            "probability": probability,
            "predicted_date": predicted_date,
            "prediction_timestamp": datetime.now().isoformat(),
            "validated": False
        })
    
    def log_actual_failure(
        self,
        vehicle_id: str,
        component: str,
        failure_date: str,
        root_cause: Optional[str] = None
    ):
        """Log an actual failure."""
        self.failure_history.append({
            "vehicle_id": vehicle_id,
            "component": component,
            "failure_date": failure_date,
            "root_cause": root_cause,
            "logged_at": datetime.now().isoformat()
        })
    
    def generate_rca_report(
        self,
        component: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate RCA report for failures.
        
        Args:
            component: Specific component (optional)
            days: Days to analyze
        
        Returns:
            RCA report with insights
        """
        # Filter failures
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_failures = [
            f for f in self.failure_history
            if datetime.fromisoformat(f["logged_at"]) >= cutoff_date
        ]
        
        if component:
            recent_failures = [f for f in recent_failures if f["component"] == component]
        
        # If no real data, generate mock insights
        if not recent_failures:
            return self._generate_mock_rca_report(component)
        
        # Analyze patterns
        component_counts = Counter(f["component"] for f in recent_failures)
        vehicle_counts = Counter(f["vehicle_id"] for f in recent_failures)
        
        # Find recurring issues
        recurring_vehicles = [v for v, count in vehicle_counts.items() if count > 1]
        
        # Calculate recurrence rate
        total_vehicles = len(set(f["vehicle_id"] for f in recent_failures))
        recurrence_rate = len(recurring_vehicles) / max(total_vehicles, 1)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            component_counts,
            recurrence_rate,
            component
        )
        
        return {
            "report_id": f"RCA-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "analysis_period_days": days,
            "component_focus": component or "all",
            "total_failures": len(recent_failures),
            "component_distribution": dict(component_counts),
            "most_common_component": component_counts.most_common(1)[0] if component_counts else None,
            "recurring_vehicles": recurring_vehicles,
            "recurrence_rate": round(recurrence_rate, 2),
            "recommendations": recommendations,
            "severity": self._calculate_severity(recurrence_rate, len(recent_failures))
        }
    
    def validate_predictions(self) -> Dict[str, Any]:
        """
        Validate predictions against actual failures.
        
        Returns:
            Validation metrics
        """
        validated_count = 0
        true_positives = 0
        false_positives = 0
        
        for prediction in self.prediction_history:
            if prediction["validated"]:
                continue
            
            # Check if there's a matching failure
            matching_failures = [
                f for f in self.failure_history
                if f["vehicle_id"] == prediction["vehicle_id"]
                and f["component"] == prediction["component"]
            ]
            
            if matching_failures:
                true_positives += 1
                prediction["validated"] = True
            else:
                # Check if prediction date has passed
                pred_date = datetime.fromisoformat(prediction["predicted_date"])
                if datetime.now() > pred_date + timedelta(days=7):
                    false_positives += 1
                    prediction["validated"] = True
            
            if prediction["validated"]:
                validated_count += 1
        
        total_validated = validated_count
        accuracy = true_positives / max(total_validated, 1)
        
        return {
            "total_predictions": len(self.prediction_history),
            "validated_predictions": total_validated,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "accuracy": round(accuracy, 2),
            "precision": round(true_positives / max(true_positives + false_positives, 1), 2)
        }
    
    def _generate_mock_rca_report(self, component: Optional[str]) -> Dict[str, Any]:
        """Generate mock RCA report for demo."""
        component = component or "brake_system"
        
        mock_data = {
            "brake_system": {
                "recurrence_rate": 0.32,
                "root_cause": "Supplier X brake pad material degradation in high-temperature conditions",
                "affected_batch": "Q2-2024",
                "recommendation": "Switch to heat-resistant brake pad compound. Increase material tolerance by +5%."
            },
            "engine": {
                "recurrence_rate": 0.18,
                "root_cause": "Coolant pump bearing failure in vehicles with >80,000 km",
                "affected_batch": "Q1-2023",
                "recommendation": "Implement preventive coolant pump replacement at 75,000 km service."
            },
            "battery": {
                "recurrence_rate": 0.25,
                "root_cause": "Battery degradation accelerated in hot climate regions",
                "affected_batch": "Q3-2024",
                "recommendation": "Use climate-optimized battery chemistry for hot regions."
            },
            "tyre": {
                "recurrence_rate": 0.15,
                "root_cause": "Uneven wear due to alignment issues in specific vehicle models",
                "affected_batch": "All batches",
                "recommendation": "Include complimentary alignment check with tyre service."
            }
        }
        
        data = mock_data.get(component, mock_data["brake_system"])
        
        return {
            "report_id": f"RCA-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "analysis_period_days": 30,
            "component_focus": component,
            "total_failures": 50,
            "recurrence_rate": data["recurrence_rate"],
            "root_cause": data["root_cause"],
            "affected_batch": data["affected_batch"],
            "recommendations": [
                {
                    "type": "CORRECTIVE_ACTION",
                    "action": data["recommendation"],
                    "priority": "HIGH",
                    "estimated_impact": "Reduce failures by 60-80%"
                },
                {
                    "type": "PREVENTIVE_ACTION",
                    "action": f"Implement enhanced quality control for {component} components",
                    "priority": "MEDIUM",
                    "estimated_impact": "Prevent future batch issues"
                }
            ],
            "severity": "HIGH" if data["recurrence_rate"] > 0.25 else "MEDIUM"
        }
    
    def _generate_recommendations(
        self,
        component_counts: Counter,
        recurrence_rate: float,
        component: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        if recurrence_rate > 0.3:
            recommendations.append({
                "type": "CORRECTIVE_ACTION",
                "action": f"Investigate supplier quality for {component or 'top failing components'}",
                "priority": "HIGH",
                "estimated_impact": "Reduce recurrence by 50%"
            })
        
        if component_counts:
            top_component = component_counts.most_common(1)[0][0]
            recommendations.append({
                "type": "PREVENTIVE_ACTION",
                "action": f"Implement enhanced monitoring for {top_component}",
                "priority": "MEDIUM",
                "estimated_impact": "Early detection of issues"
            })
        
        return recommendations
    
    def _calculate_severity(self, recurrence_rate: float, failure_count: int) -> str:
        """Calculate severity level."""
        if recurrence_rate > 0.4 or failure_count > 100:
            return "CRITICAL"
        elif recurrence_rate > 0.25 or failure_count > 50:
            return "HIGH"
        elif recurrence_rate > 0.15 or failure_count > 20:
            return "MEDIUM"
        else:
            return "LOW"


# Global RCA insights instance
_rca_insights = None


def get_rca_insights() -> RCAInsights:
    """Get singleton RCA insights instance."""
    global _rca_insights
    if _rca_insights is None:
        _rca_insights = RCAInsights()
    return _rca_insights
