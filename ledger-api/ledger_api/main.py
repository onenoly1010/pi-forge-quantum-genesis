"""
Ledger API - Main FastAPI Application
Multi-Account Treasury System with Atomic Allocations
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import database components
from ledger_api.db import engine, Base
from ledger_api.models import ledger_models  # Import to register models

# Import API routers
from ledger_api.api.v1 import (
    transactions,
    treasury,
    reconcile,
    allocation_rules
)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting Ledger API...")
    
    # Environment validation
    app_env = os.getenv("APP_ENVIRONMENT", "development")
    logger.info(f"Environment: {app_env}")
    
    # Security check: NFT_MINT_VALUE must be 0 for non-mainnet
    nft_mint_value = int(os.getenv("NFT_MINT_VALUE", "0"))
    if app_env != "mainnet" and nft_mint_value != 0:
        raise RuntimeError(
            f"SECURITY: NFT_MINT_VALUE must be 0 in {app_env} environment. "
            f"Current value: {nft_mint_value}"
        )
    
    # Create database tables if they don't exist
    # Note: In production, use Alembic migrations instead
    if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true" and not os.getenv("TESTING"):
        logger.warning("Auto-creating database tables (use Alembic migrations in production)")
        Base.metadata.create_all(bind=engine)
    
    logger.info("Ledger API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Ledger API...")


# Create FastAPI app
app = FastAPI(
    title="Ledger API",
    description="Multi-Account Treasury System with Atomic Allocations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(transactions.router)
app.include_router(treasury.router)
app.include_router(reconcile.router)
app.include_router(allocation_rules.router)


# Root endpoint
@app.get("/")
def read_root():
    """Health check and API info"""
    return {
        "service": "Ledger API",
        "version": "1.0.0",
        "status": "healthy",
        "environment": os.getenv("APP_ENVIRONMENT", "development"),
        "nft_mint_value": int(os.getenv("NFT_MINT_VALUE", "0"))
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB health check
        "environment": os.getenv("APP_ENVIRONMENT", "development")
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8001"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("APP_ENVIRONMENT") == "development"
    )
