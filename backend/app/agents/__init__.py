"""
Agent framework for AuroraSync OS.
Multi-agent orchestration system for predictive maintenance.
"""

from app.agents.base_agent import BaseAgent
from app.agents.master_agent import MasterAgent, get_master_agent
from app.agents.data_analysis_agent import DataAnalysisAgent
from app.agents.diagnosis_agent import DiagnosisAgent
from app.agents.customer_engagement_agent import CustomerEngagementAgent
from app.agents.scheduling_agent import SchedulingAgent
from app.agents.feedback_agent import FeedbackAgent
from app.agents.manufacturing_insights_agent import ManufacturingInsightsAgent
from app.agents.ueba_agent import UEBAAgent

__all__ = [
    "BaseAgent",
    "MasterAgent",
    "get_master_agent",
    "DataAnalysisAgent",
    "DiagnosisAgent",
    "CustomerEngagementAgent",
    "SchedulingAgent",
    "FeedbackAgent",
    "ManufacturingInsightsAgent",
    "UEBAAgent",
]
