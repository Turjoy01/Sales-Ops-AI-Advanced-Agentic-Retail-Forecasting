"""
Model Info API Endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ModelInfoResponse
from app.models.ml_models import model_loader
from app.config import settings

router = APIRouter(prefix="/api/v1/models", tags=["Models"])

@router.get("/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get model metadata and training info"""
    try:
        ensemble_config, risk_config = model_loader.get_config()
        hist_data = model_loader.get_historical_data()
        
        return {
            "last_training_date": "2024-01-01",  # This would ideally come from config
            "model_version": "1.2.0",
            "weights": {
                "prophet": settings.WEIGHT_PROPHET,
                "sarima": settings.WEIGHT_SARIMA
            },
            "total_training_samples": len(hist_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
