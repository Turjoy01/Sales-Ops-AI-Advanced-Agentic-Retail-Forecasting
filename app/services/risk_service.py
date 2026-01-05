"""
Risk Assessment Service
"""
from app.models.ml_models import model_loader

class RiskService:
    """Risk assessment service"""
    
    def __init__(self):
        self.historical_data = model_loader.get_historical_data()
    
    def assess_risk(self, forecast_value: float, date: str, confidence_interval: dict = None) -> dict:
        """
        Assess risk of forecast
        
        Args:
            forecast_value: Predicted sales
            date: Date string
            confidence_interval: Optional CI dict
        
        Returns:
            Risk assessment dict
        """
        hist_sales = self.historical_data['Sales']
        hist_mean = hist_sales.mean()
        hist_std = hist_sales.std()
        recent_mean = hist_sales[-30:].mean()
        
        # Deviations
        deviation_pct = ((forecast_value - hist_mean) / hist_mean) * 100
        recent_deviation_pct = ((forecast_value - recent_mean) / recent_mean) * 100
        
        # CI width
        ci_width_pct = None
        if confidence_interval:
            ci_range = confidence_interval['upper'] - confidence_interval['lower']
            ci_width_pct = (ci_range / forecast_value) * 100
        
        # Calculate risk score
        risk_score = 0
        factors = []
        
        # Large deviation
        if abs(deviation_pct) > 50:
            risk_score += 30
            factors.append(f"Large deviation from mean ({deviation_pct:+.1f}%)")
        elif abs(deviation_pct) > 25:
            risk_score += 15
        
        # Recent trend deviation
        if abs(recent_deviation_pct) > 30:
            risk_score += 25
            factors.append(f"Deviates from recent trend ({recent_deviation_pct:+.1f}%)")
        
        # Wide CI
        if ci_width_pct and ci_width_pct > 100:
            risk_score += 30
            factors.append(f"Wide confidence interval ({ci_width_pct:.0f}%)")
        elif ci_width_pct and ci_width_pct > 50:
            risk_score += 15
        
        # Volatility
        cv = hist_std / hist_mean
        if cv > 1.0:
            risk_score += 15
            factors.append(f"High volatility (CV={cv:.2f})")
        
        # Risk level
        if risk_score >= 70:
            risk_level = 'High'
            reliability = 'Low'
        elif risk_score >= 40:
            risk_level = 'Medium'
            reliability = 'Medium'
        else:
            risk_level = 'Low'
            reliability = 'High'
        
        return {
            'date': date,
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'reliability': reliability,
            'deviation_from_mean': deviation_pct,
            'risk_factors': factors
        }
    
    def get_historical_analysis(self, start_date: str = None, end_date: str = None) -> list:
        """Get historical risk analysis or generate new predictions for future dates"""
        import pandas as pd
        from app.config import settings
        from app.services.forecast_service import forecast_service
        
        results = []
        try:
            # 1. Load Historical Data from CSV
            analysis_path = settings.MODEL_DIR / "risk_analysis.csv"
            if analysis_path.exists():
                df = pd.read_csv(analysis_path)
                df = df.rename(columns={'Order Date': 'date', 'Sales': 'forecast_value'})
                df['date'] = df['date'].astype(str)
                
                # Filter historical data if range provided
                if start_date:
                    df = df[df['date'] >= start_date]
                if end_date:
                    df = df[df['date'] <= end_date]
                
                results = df.to_dict(orient='records')

            # 2. Check if we need to generate future predictions
            # If end_date is after the last date in our CSV (2018-12-30), we generate more
            last_hist_date = "2018-12-30" # The training data boundary
            
            check_date = end_date if end_date else pd.Timestamp.now().strftime('%Y-%m-%d')
            
            if check_date > last_hist_date:
                # Determine the range for generation
                # FIXED: Don't start from 2018 if no start_date is provided!
                # Instead, use a reasonable default (e.g., 30 days ago or last_hist_date)
                if start_date and start_date > last_hist_date:
                    gen_start = start_date
                else:
                    # Default: start from 30 days ago (or last_hist_date if that's more recent)
                    default_start = (pd.Timestamp.now() - pd.Timedelta(days=30)).strftime('%Y-%m-%d')
                    gen_start = max(default_start, last_hist_date)
                    # Increment by one day to avoid overlap with historical data
                    if gen_start == last_hist_date:
                        gen_start = (pd.to_datetime(last_hist_date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                
                gen_end = check_date
                
                # Safety limit: prevent generating more than 90 days at once
                date_diff = (pd.to_datetime(gen_end) - pd.to_datetime(gen_start)).days
                if date_diff > 90:
                    print(f"⚠️ Requested range too large ({date_diff} days). Limiting to 90 days from start date.")
                    gen_end = (pd.to_datetime(gen_start) + pd.Timedelta(days=90)).strftime('%Y-%m-%d')
                
                # To prevent excessive processing, limit the range if it's too large
                # For example, if no end_date is provided, we only predict for the next 7 days
                if not end_date:
                    gen_end = (pd.Timestamp.now() + pd.Timedelta(days=7)).strftime('%Y-%m-%d')
                
                if gen_start <= gen_end:
                    print(f"🔮 Generating dynamic future risks from {gen_start} to {gen_end}...")
                    future_predictions = forecast_service.batch_predict(gen_start, gen_end)
                    
                    for pred in future_predictions:
                        risk = self.assess_risk(
                            pred['ensemble_prediction'],
                            pred['date'],
                            pred.get('confidence_interval')
                        )
                        results.append({
                            'date': pred['date'],
                            'forecast_value': pred['ensemble_prediction'],
                            'risk_score': risk['risk_score'],
                            'risk_level': risk['risk_level'],
                            'risk_factors': "; ".join(risk['risk_factors']) if risk['risk_factors'] else "Stable forecast"
                        })

            # Sort by date descending
            results.sort(key=lambda x: x['date'], reverse=True)
            return results
            
        except Exception as e:
            print(f"Error in dynamic risk analysis: {e}")
            return results

risk_service = RiskService()
