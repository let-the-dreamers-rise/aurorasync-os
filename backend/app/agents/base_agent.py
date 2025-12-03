"""
Base Agent class for AuroraSync OS.
All agents inherit from this abstract base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from datetime import datetime


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Each agent must implement the handle_event method to process events.
    This provides a consistent interface for the Master Agent to interact
    with all worker agents.
    
    Attributes:
        name: Unique name of the agent (e.g., "data_analysis", "diagnosis")
        logger: Logger instance for this agent
    """
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: Unique identifier for this agent
        """
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
        self.logger.info(f"🤖 Agent '{name}' initialized")
    
    @abstractmethod
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an incoming event.
        
        This method must be implemented by all subclasses.
        It processes the event and returns a response.
        
        Args:
            event: Event dictionary containing:
                - type: Event type (e.g., "analyze_data", "predict_failure")
                - payload: Event-specific data
                - timestamp: When the event was created
                - source: Where the event came from
        
        Returns:
            Response dictionary containing:
                - status: "success" or "error"
                - agent: Name of the agent that processed the event
                - result: Processing result
                - timestamp: When the response was created
        
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError(f"Agent '{self.name}' must implement handle_event()")
    
    def log_event(self, event: Dict[str, Any], action: str = "received") -> None:
        """
        Log an event for debugging and monitoring.
        
        Args:
            event: Event to log
            action: Action being performed (e.g., "received", "processed", "sent")
        """
        event_type = event.get("type", "unknown")
        self.logger.debug(f"Event {action}: type={event_type}, agent={self.name}")
    
    def create_response(
        self,
        status: str,
        result: Any = None,
        error: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized response dictionary.
        
        Args:
            status: Response status ("success" or "error")
            result: Processing result (optional)
            error: Error message if status is "error" (optional)
            metadata: Additional metadata (optional)
        
        Returns:
            Standardized response dictionary
        """
        response = {
            "status": status,
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if result is not None:
            response["result"] = result
        
        if error is not None:
            response["error"] = error
        
        if metadata is not None:
            response["metadata"] = metadata
        
        return response
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"<{self.__class__.__name__}(name='{self.name}')>"
