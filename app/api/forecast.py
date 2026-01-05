"""
Forecast API Endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PredictRequest, BatchPredictRequest,
    PredictionResponse
)
from app.services.forecast_service import forecast_service

router = APIRouter(prefix="/api/v1/forecast", tags=["Forecast"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_single(request: PredictRequest):
    """Predict sales for a single date"""
    try:
        result = forecast_service.predict(request.date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch")
async def predict_batch(request: BatchPredictRequest):
    """Predict sales for date range"""
    try:
        results = forecast_service.batch_predict(request.start_date, request.end_date)
        return {
            "start_date": request.start_date,
            "end_date": request.end_date,
            "total_predictions": len(results),
            "predictions": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/next-week")
async def next_week():
    """Predict next 7 days"""
    try:
        result = forecast_service.next_week_forecast()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))