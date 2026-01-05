"""
Decision Engine API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.decision_service import decision_service

router = APIRouter(prefix="/api/v1/decisions", tags=["Decisions"])

class DecisionRequest(BaseModel):
    date: str
    forecast: float
    risk_score: int
    reliability: str
    is_anomaly: Optional[bool] = False

class DecisionResponse(BaseModel):
    actions: List[str]
    priority: str
    reason: str

@router.post("/evaluate", response_model=DecisionResponse)
async def evaluate_decision(request: DecisionRequest):
    """Evaluate business rules for a forecast"""
    try:
        risk_data = {
            "risk_score": request.risk_score,
            "reliability": request.reliability,
            "is_anomaly": request.is_anomaly
        }
        return decision_service.evaluate(request.forecast, risk_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
