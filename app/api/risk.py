"""
Risk Assessment API Endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import RiskAssessRequest, RiskResponse
from app.services.risk_service import risk_service

router = APIRouter(prefix="/api/v1/risk", tags=["Risk"])

@router.post("/assess", response_model=RiskResponse)
async def assess_risk(request: RiskAssessRequest):
    """Assess risk of a forecast"""
    try:
        result = risk_service.assess_risk(
            request.forecast_value,
            request.date,
            request.confidence_interval
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- New Sales Intelligence Agent Features ---

@router.get("/deals/open")
async def get_open_deals():
    """Fetch open deals from Salesforce (Feature 2)"""
    from app.services.salesforce_service import salesforce_service
    return salesforce_service.get_open_opportunities()

@router.post("/deals/score")
async def score_deal(opportunity: dict):
    """Score a specific deal using XGBoost (Feature 2)"""
    from app.services.deal_risk_service import deal_risk_service
    return deal_risk_service.predict_risk(opportunity)

@router.post("/deals/insights")
async def get_deal_insights(opportunity: dict):
    """Generate AI insights for a deal (Feature 3)"""
    from app.services.deal_risk_service import deal_risk_service
    from app.services.llm_service import llm_service
    risk_data = deal_risk_service.predict_risk(opportunity)
    return {
        "risk_data": risk_data,
        "insights": llm_service.generate_deal_insights(opportunity, risk_data)
    }

@router.post("/automation/run-daily")
async def run_daily_pipeline():
    """Trigger the daily automation pipeline (Feature 4 & 5)"""
    from app.services.automation_service import automation_service
    return await automation_service.run_daily_pipeline()

@router.get("/analysis")
async def get_risk_analysis(start_date: str = None, end_date: str = None):
    """Get historical risk analysis"""
    try:
        return risk_service.get_historical_analysis(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))