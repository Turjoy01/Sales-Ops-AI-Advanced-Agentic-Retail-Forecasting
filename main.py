"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import forecast, risk, reports, models_info
from app.models.schemas import HealthResponse
from app.models.ml_models import model_loader
from app.config import settings
import os

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Advanced Retail Sales Forecasting System with Ensemble ML Models"
)

# Static files and Frontend
# Ensure we have absolute paths for static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
PAGES_DIR = os.path.join(FRONTEND_DIR, "pages")
app.mount("/pages", StaticFiles(directory=PAGES_DIR), name="pages")

@app.get("/", tags=["Frontend"])
async def read_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Include API routers
app.include_router(forecast.router)
app.include_router(risk.router)
app.include_router(reports.router)
app.include_router(models_info.router)
# New Routers
from app.api import decisions, integrations
app.include_router(decisions.router)
app.include_router(integrations.router)

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """API Health Check"""
    return {
        "status": "healthy",
        "models_loaded": model_loader._models_loaded,
        "api_version": settings.API_VERSION
    }

# Run app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)