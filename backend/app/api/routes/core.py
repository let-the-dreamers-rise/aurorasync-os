"""
Core API routes for health checks and system information.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from app.database import get_db
from app.config import settings


router = APIRouter()


@router.get("/health", tags=["Core"])
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    Returns the current status of the API.
    
    Returns:
        dict: Status message
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/info", tags=["Core"])
def system_info() -> Dict[str, Any]:
    """
    System information endpoint.
    Returns project name, version, and configuration details.
    
    Returns:
        dict: System information
    """
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "api_prefix": settings.API_V1_PREFIX,
        "description": "The Self-Healing Vehicle Brain - AI-powered predictive maintenance system"
    }


@router.get("/db-check", tags=["Core"])
def database_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Database connectivity check.
    Verifies that the database connection is working.
    
    Args:
        db: Database session (injected by FastAPI)
    
    Returns:
        dict: Database status
    """
    try:
        # Execute a simple query to check connection
        db.execute("SELECT 1")
        return {
            "status": "ok",
            "database": "connected",
            "message": "Database connection is healthy"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "message": f"Database connection failed: {str(e)}"
        }
