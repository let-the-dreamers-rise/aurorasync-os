"""
Demand Forecaster for AuroraSync OS.
Predicts service demand using time-series forecasting.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import numpy as np


logger = logging.getLogger(__name__)


class DemandForecaster:
    """
    Forecasts service demand for workshops.
    Uses simple moving average and trend analysis.
    In production, this would use Prophet or ARIMA.
    """
    
    def __init__(self):
        """Initialize demand forecaster."""
        # Historical demand data (mock)
        self.historical_demand = self._generate_mock_historical_data()
        logger.info("Demand Forecaster initialized")
    
    def _generate_mock_historical_data(self) -> Dict[str, List[int]]:
        """Generate mock historical demand data."""
        workshops = ["WS-MUM-01", "WS-PUNE-01", "WS-BLR-01", "WS-DEL-01", "WS-CHE-01"]
        data = {}
        
        for ws_id in workshops:
            # Generate 30 days of historical data
            base_demand = np.random.randint(5, 15)
            trend = np.random.choice([-0.1, 0, 0.1])
            seasonality = np.random.rand() * 3
            
            daily_demand = []
            for day in range(30):
                # Add trend and seasonality
                demand = base_demand + (trend * day) + (seasonality * np.sin(day / 7 * 2 * np.pi))
                demand = max(0, int(demand + np.random.randn() * 2))
                daily_demand.append(demand)
            
            data[ws_id] = daily_demand
        
        return data
    
    def forecast_demand(
        self,
        workshop_id: str,
        days_ahead: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Forecast demand for a workshop.
        
        Args:
            workshop_id: Workshop ID
            days_ahead: Number of days to forecast
        
        Returns:
            List of daily forecasts
        """
        if workshop_id not in self.historical_demand:
            # Return default forecast
            return self._default_forecast(days_ahead)
        
        historical = self.historical_demand[workshop_id]
        
        # Simple moving average forecast
        window_size = 7
        recent_data = historical[-window_size:]
        avg_demand = np.mean(recent_data)
        trend = (recent_data[-1] - recent_data[0]) / window_size
        
        forecasts = []
        for day in range(days_ahead):
            # Forecast with trend
            forecast_value = avg_demand + (trend * day)
            
            # Add day-of-week seasonality
            future_date = datetime.now() + timedelta(days=day)
            day_of_week = future_date.weekday()
            
            # Weekend adjustment (lower demand)
            if day_of_week >= 5:
                forecast_value *= 0.7
            
            # Monday adjustment (higher demand)
            if day_of_week == 0:
                forecast_value *= 1.2
            
            forecast_value = max(0, int(forecast_value))
            
            # Calculate confidence interval
            std_dev = np.std(recent_data)
            lower_bound = max(0, int(forecast_value - std_dev))
            upper_bound = int(forecast_value + std_dev)
            
            forecasts.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "day_of_week": future_date.strftime("%A"),
                "forecast_demand": forecast_value,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "confidence": 0.85
            })
        
        return forecasts
    
    def predict_optimal_slot(
        self,
        workshop_id: str,
        component: str,
        risk_level: str
    ) -> Dict[str, Any]:
        """
        Predict optimal time slot based on forecasted demand.
        
        Args:
            workshop_id: Workshop ID
            component: Component type
            risk_level: Risk level
        
        Returns:
            Optimal slot recommendation
        """
        forecasts = self.forecast_demand(workshop_id, days_ahead=7)
        
        # Find day with lowest forecasted demand
        min_demand_day = min(forecasts, key=lambda x: x["forecast_demand"])
        
        # Adjust based on risk level
        if risk_level == "high":
            # Recommend earliest available
            recommended_day = forecasts[0]
            reasoning = "High risk requires immediate attention"
        elif risk_level == "medium":
            # Recommend within 3 days, prefer low demand
            candidates = forecasts[:3]
            recommended_day = min(candidates, key=lambda x: x["forecast_demand"])
            reasoning = "Medium risk, balanced with workshop load"
        else:
            # Recommend lowest demand day
            recommended_day = min_demand_day
            reasoning = "Low risk, optimized for minimal wait time"
        
        return {
            "recommended_date": recommended_day["date"],
            "forecast_demand": recommended_day["forecast_demand"],
            "reasoning": reasoning,
            "alternative_dates": [f["date"] for f in forecasts[:3]]
        }
    
    def get_workshop_load_curve(
        self,
        workshop_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get predicted load curve for a workshop.
        
        Args:
            workshop_id: Workshop ID
            days: Number of days
        
        Returns:
            Load curve data
        """
        forecasts = self.forecast_demand(workshop_id, days)
        
        # Calculate load percentages (assuming capacity of 10 per day)
        capacity = 10
        load_curve = []
        
        for forecast in forecasts:
            load_percentage = min(100, (forecast["forecast_demand"] / capacity) * 100)
            
            if load_percentage < 50:
                status = "low"
            elif load_percentage < 80:
                status = "moderate"
            else:
                status = "high"
            
            load_curve.append({
                "date": forecast["date"],
                "demand": forecast["forecast_demand"],
                "capacity": capacity,
                "load_percentage": round(load_percentage, 1),
                "status": status
            })
        
        return {
            "workshop_id": workshop_id,
            "load_curve": load_curve,
            "average_load": round(np.mean([lc["load_percentage"] for lc in load_curve]), 1),
            "peak_day": max(load_curve, key=lambda x: x["load_percentage"])
        }
    
    def _default_forecast(self, days_ahead: int) -> List[Dict[str, Any]]:
        """Generate default forecast."""
        forecasts = []
        for day in range(days_ahead):
            future_date = datetime.now() + timedelta(days=day)
            forecasts.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "day_of_week": future_date.strftime("%A"),
                "forecast_demand": 8,
                "lower_bound": 5,
                "upper_bound": 11,
                "confidence": 0.70
            })
        return forecasts


# Global demand forecaster instance
_demand_forecaster = None


def get_demand_forecaster() -> DemandForecaster:
    """Get singleton demand forecaster instance."""
    global _demand_forecaster
    if _demand_forecaster is None:
        _demand_forecaster = DemandForecaster()
    return _demand_forecaster
