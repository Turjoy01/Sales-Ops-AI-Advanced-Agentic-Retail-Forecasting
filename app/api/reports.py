"""
Report Generation API Endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.schemas import ReportRequest, ReportResponse
from app.services.forecast_service import forecast_service
from app.services.risk_service import risk_service
from app.services.llm_service import llm_service
from app.services.email_service import email_service

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.post("/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """Generate full forecast report with AI explanation"""
    try:
        # Get forecast
        forecast = forecast_service.predict(request.date)
        
        # Get risk
        risk = risk_service.assess_risk(
            forecast['ensemble_prediction'],
            request.date,
            forecast.get('confidence_interval')
        )
        
        # Generate explanation
        explanation = llm_service.generate_explanation(forecast, risk)
        
        # Build report
        report = {
            'date': request.date,
            'forecast': forecast,
            'risk': risk,
            'explanation': explanation,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Send email if requested
        if request.send_email:
            recipient = request.recipient_email
            email_service.send_report(report, recipient)
        
        return report
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/email")
async def email_report(request: ReportRequest):
    """Generate and email report"""
    request.send_email = True
    return await generate_report(request)

@router.get("/weekly")
async def weekly_report():
    """Generate 7-day forecast summary"""
    try:
        forecast_data = forecast_service.next_week_forecast()
        
        reports = []
        for pred in forecast_data['predictions']:
            risk = risk_service.assess_risk(
                pred['ensemble_prediction'],
                pred['date'],
                pred.get('confidence_interval')
            )
            reports.append({
                'date': pred['date'],
                'forecast': pred['ensemble_prediction'],
                'risk_level': risk['risk_level'],
                'risk_score': risk['risk_score']
            })
        
        return {
            'summary': forecast_data,
            'detailed_reports': reports
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))