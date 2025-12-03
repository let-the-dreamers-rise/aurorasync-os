"""
AuroraSync OS - FastAPI Application Entry Point
The Self-Healing Vehicle Brain

This is the main application file that initializes FastAPI,
configures middleware, and registers all API routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.api.routes import core, agents, predictions, voice, scheduling


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered predictive maintenance system for vehicles with multi-agent orchestration",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Configure CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - Welcome message.
    """
    return {
        "message": "Welcome to AuroraSync OS API",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint (at root level for load balancers)
@app.get("/health", tags=["Root"])
def health():
    """
    Health check endpoint at root level.
    Used by load balancers and monitoring tools.
    """
    return {"status": "ok"}


# Include API routers
app.include_router(
    core.router,
    prefix=settings.API_V1_PREFIX,
    tags=["API v1"]
)

app.include_router(
    agents.router,
    prefix=f"{settings.API_V1_PREFIX}/agents",
    tags=["Agents"]
)

app.include_router(
    predictions.router,
    prefix=f"{settings.API_V1_PREFIX}/predict",
    tags=["Predictions"]
)

app.include_router(
    voice.router,
    prefix=f"{settings.API_V1_PREFIX}/voice",
    tags=["Voice"]
)

app.include_router(
    scheduling.router,
    prefix=f"{settings.API_V1_PREFIX}/scheduling",
    tags=["Scheduling"]
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    Runs when the application starts.
    """
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔗 API Prefix: {settings.API_V1_PREFIX}")
    logger.info(f"🌐 CORS Origins: {', '.join(settings.CORS_ORIGINS)}")
    logger.info("✅ Application startup complete")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    Runs when the application shuts down.
    """
    logger.info("🛑 Shutting down AuroraSync OS")
    logger.info("✅ Application shutdown complete")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.ENVIRONMENT == "development" else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
