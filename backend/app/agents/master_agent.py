"""
Master Agent - Orchestrator for all worker agents.
Routes events to appropriate agents and coordinates workflows.
"""

from typing import Dict, Any, Optional
import logging

from app.agents.base_agent import BaseAgent
from app.agents.ueba_agent import UEBAAgent


class MasterAgent(BaseAgent):
    """
    Master Agent orchestrates all worker agents.
    
    Responsibilities:
    - Route events to appropriate worker agents
    - Coordinate multi-agent workflows
    - Monitor agent health
    - Integrate with UEBA for security monitoring
    
    The Master Agent maintains a registry of all worker agents and
    routes events based on event type.
    """
    
    def __init__(self):
        """Initialize the Master Agent with worker agent registry."""
        super().__init__(name="master")
        
        # Initialize UEBA agent for monitoring
        self.ueba_agent = UEBAAgent()
        
        # Registry of worker agents (will be populated lazily)
        self._worker_agents: Dict[str, BaseAgent] = {}
        
        # Event type to agent mapping
        self._event_routing: Dict[str, str] = {
            # Data Analysis Agent
            "analyze_data": "data_analysis",
            "extract_features": "data_analysis",
            "detect_anomaly": "data_analysis",
            
            # Diagnosis Agent
            "predict_failure": "diagnosis",
            "diagnose_issue": "diagnosis",
            "assess_risk": "diagnosis",
            
            # Customer Engagement Agent
            "engage_customer": "customer_engagement",
            "generate_call_script": "customer_engagement",
            "send_notification": "customer_engagement",
            
            # Scheduling Agent
            "schedule_service": "scheduling",
            "find_availability": "scheduling",
            "book_appointment": "scheduling",
            
            # Feedback Agent
            "validate_prediction": "feedback",
            "collect_feedback": "feedback",
            "calculate_accuracy": "feedback",
            
            # Manufacturing Insights Agent
            "generate_rca": "manufacturing_insights",
            "create_capa": "manufacturing_insights",
            "analyze_patterns": "manufacturing_insights",
            
            # UEBA Agent
            "get_ueba_stats": "ueba",
            "check_anomaly": "ueba",
            
            # Voice Agent (via Customer Engagement)
            "voice_predict_failure": "customer_engagement",
            "voice_urgent_alert": "customer_engagement",
            "voice_reminder": "customer_engagement",
            "voice_feedback": "customer_engagement",
            "voice_booking_recovery": "customer_engagement",
        }
        
        self.logger.info("🎯 Master Agent initialized with event routing")
    
    def _get_worker_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        Get or create a worker agent.
        
        Lazy initialization of worker agents to avoid circular imports
        and unnecessary initialization.
        
        Args:
            agent_name: Name of the worker agent
        
        Returns:
            Worker agent instance or None if not found
        """
        # Return if already initialized
        if agent_name in self._worker_agents:
            return self._worker_agents[agent_name]
        
        # Return UEBA agent directly
        if agent_name == "ueba":
            return self.ueba_agent
        
        # Lazy import and initialize worker agents
        try:
            if agent_name == "data_analysis":
                from app.agents.data_analysis_agent import DataAnalysisAgent
                self._worker_agents[agent_name] = DataAnalysisAgent()
            
            elif agent_name == "diagnosis":
                from app.agents.diagnosis_agent import DiagnosisAgent
                self._worker_agents[agent_name] = DiagnosisAgent()
            
            elif agent_name == "customer_engagement":
                from app.agents.customer_engagement_agent import CustomerEngagementAgent
                self._worker_agents[agent_name] = CustomerEngagementAgent()
            
            elif agent_name == "scheduling":
                from app.agents.scheduling_agent import SchedulingAgent
                self._worker_agents[agent_name] = SchedulingAgent()
            
            elif agent_name == "feedback":
                from app.agents.feedback_agent import FeedbackAgent
                self._worker_agents[agent_name] = FeedbackAgent()
            
            elif agent_name == "manufacturing_insights":
                from app.agents.manufacturing_insights_agent import ManufacturingInsightsAgent
                self._worker_agents[agent_name] = ManufacturingInsightsAgent()
            
            else:
                self.logger.error(f"Unknown agent: {agent_name}")
                return None
            
            return self._worker_agents[agent_name]
        
        except Exception as e:
            self.logger.error(f"Error initializing agent '{agent_name}': {e}")
            return None
    
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle events directed to the Master Agent.
        
        Args:
            event: Event to process
        
        Returns:
            Response dictionary
        """
        self.log_event(event, "received")
        
        event_type = event.get("type", "unknown")
        
        if event_type == "get_agent_status":
            # Return status of all agents
            return self.create_response(
                status="success",
                result=self.get_agent_status()
            )
        
        # Default: route to appropriate worker agent
        return self.route_event(event)
    
    def route_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route an event to the appropriate worker agent.
        
        This is the main orchestration method. It:
        1. Determines which agent should handle the event
        2. Logs the action with UEBA
        3. Forwards the event to the worker agent
        4. Returns the response
        
        Args:
            event: Event to route
        
        Returns:
            Response from the worker agent
        """
        event_type = event.get("type", "unknown")
        
        # Log the routing action with UEBA
        self.ueba_agent.log_action(
            agent_name="master",
            action="route_event",
            resource=event_type,
            metadata={"event": event}
        )
        
        # Determine target agent
        target_agent_name = self._event_routing.get(event_type)
        
        if not target_agent_name:
            self.logger.warning(f"No routing rule for event type: {event_type}")
            return self.create_response(
                status="error",
                error=f"Unknown event type: {event_type}",
                metadata={"available_types": list(self._event_routing.keys())}
            )
        
        # Get the worker agent
        worker_agent = self._get_worker_agent(target_agent_name)
        
        if not worker_agent:
            return self.create_response(
                status="error",
                error=f"Worker agent '{target_agent_name}' not available"
            )
        
        # Log the delegation with UEBA
        self.ueba_agent.log_action(
            agent_name=target_agent_name,
            action="handle_event",
            resource=event_type,
            metadata={"delegated_by": "master"}
        )
        
        # Forward event to worker agent
        self.logger.info(f"📤 Routing event '{event_type}' to agent '{target_agent_name}'")
        
        try:
            response = worker_agent.handle_event(event)
            self.logger.info(f"✅ Agent '{target_agent_name}' processed event successfully")
            return response
        
        except Exception as e:
            self.logger.error(f"❌ Agent '{target_agent_name}' failed: {e}")
            return self.create_response(
                status="error",
                error=f"Agent '{target_agent_name}' failed: {str(e)}"
            )
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status of all agents.
        
        Returns:
            Dictionary with agent status information
        """
        return {
            "master_agent": {
                "status": "active",
                "name": self.name,
                "worker_agents_initialized": len(self._worker_agents)
            },
            "worker_agents": {
                "data_analysis": "available",
                "diagnosis": "available",
                "customer_engagement": "available",
                "scheduling": "available",
                "feedback": "available",
                "manufacturing_insights": "available",
                "ueba": "active"
            },
            "event_routing": {
                "total_routes": len(self._event_routing),
                "available_event_types": list(self._event_routing.keys())
            },
            "ueba_stats": self.ueba_agent.get_statistics()
        }


# Singleton instance
_master_agent_instance: Optional[MasterAgent] = None


def get_master_agent() -> MasterAgent:
    """
    Get the singleton Master Agent instance.
    
    This ensures only one Master Agent exists in the application,
    which is important for maintaining consistent state and monitoring.
    
    Returns:
        Master Agent singleton instance
    """
    global _master_agent_instance
    
    if _master_agent_instance is None:
        _master_agent_instance = MasterAgent()
        logging.getLogger("agent.master").info("🎯 Master Agent singleton created")
    
    return _master_agent_instance
