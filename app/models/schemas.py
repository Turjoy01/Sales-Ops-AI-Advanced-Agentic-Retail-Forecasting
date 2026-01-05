"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime

# ==================== Request Models ====================

class PredictRequest(BaseModel):
    """Single date prediction request"""
    date: str = Field(..., example="2019-01-15", description="Date in YYYY-MM-DD format")
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

class BatchPredictRequest(BaseModel):
    """Batch prediction request"""
    start_date: str = Field(..., example="2019-01-01")
    end_date: str = Field(..., example="2019-01-07")
    
    @validator('start_date', 'end_date')
    def validate_dates(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Dates must be in YYYY-MM-DD format')

class RiskAssessRequest(BaseModel):
    """Risk assessment request"""
    date: str
    forecast_value: float
    confidence_interval: Optional[dict] = None

class ReportRequest(BaseModel):
    """Report generation request"""
    date: str
    send_email: bool = False
    recipient_email: Optional[str] = None

# ==================== Response Models ====================

class PredictionResponse(BaseModel):
    """Prediction response"""
    date: str
    type: str  # 'historical' or 'future'
    actual_sales: Optional[float] = None
    prophet_prediction: float
    sarima_prediction: Optional[float] = None
    ensemble_prediction: float
    confidence_interval: Optional[dict] = None

class RiskResponse(BaseModel):
    """Risk assessment response"""
    date: str
    risk_score: int
    risk_level: str  # Low/Medium/High
    reliability: str
    deviation_from_mean: float
    risk_factors: List[str]

class ReportResponse(BaseModel):
    """Full report response"""
    date: str
    forecast: PredictionResponse
    risk: RiskResponse
    explanation: str
    generated_at: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    models_loaded: bool
    api_version: str

class ModelInfoResponse(BaseModel):
    """Model information response"""
    last_training_date: str
    model_version: str
    weights: dict
    total_training_samples: int