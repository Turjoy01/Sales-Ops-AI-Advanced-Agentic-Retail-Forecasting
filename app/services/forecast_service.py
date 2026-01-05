"""
Forecasting Service - Core prediction logic
"""
import pandas as pd
import warnings
from datetime import timedelta
from app.models.ml_models import model_loader
from app.config import settings

# Suppress statsmodels warnings
try:
    from statsmodels.tools.sm_exceptions import ValueWarning
    warnings.filterwarnings("ignore", category=ValueWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
except ImportError:
    pass

class ForecastService:
    """Forecasting service for sales predictions"""
    
    def __init__(self):
        self.prophet_model = model_loader.get_prophet()
        self.sarima_model = model_loader.get_sarima()
        self.historical_data = model_loader.get_historical_data()
        self.weight_prophet = settings.WEIGHT_PROPHET
        self.weight_sarima = settings.WEIGHT_SARIMA
    
    def predict(self, date_str: str) -> dict:
        """
        Generate ensemble prediction for a single date
        
        Args:
            date_str: Date in 'YYYY-MM-DD' format
        
        Returns:
            dict with prediction details
        """
        target_date = pd.to_datetime(date_str)
        last_date = self.historical_data.index[-1]
        is_historical = target_date <= last_date
        
        if is_historical:
            return self._predict_historical(target_date)
        else:
            return self._predict_future(target_date)
    
    def _predict_historical(self, target_date):
        """Predict for historical date"""
        
        # Actual value
        actual = None
        if target_date in self.historical_data.index:
            actual = float(self.historical_data.loc[target_date, 'Sales'])
        
        # Prophet
        prophet_df = pd.DataFrame({'ds': [target_date]})
        prophet_forecast = self.prophet_model.predict(prophet_df)
        prophet_pred = float(prophet_forecast['yhat'].values[0])
        
        # SARIMA
        sarima_pred = None
        try:
            if target_date in self.sarima_model.fittedvalues.index:
                sarima_pred = float(self.sarima_model.fittedvalues.loc[target_date])
        except:
            pass
        
        # Ensemble
        if sarima_pred is not None:
            ensemble = (self.weight_prophet * prophet_pred) + (self.weight_sarima * sarima_pred)
        else:
            ensemble = prophet_pred
        
        return {
            'date': target_date.strftime('%Y-%m-%d'),
            'type': 'historical',
            'actual_sales': actual,
            'prophet_prediction': prophet_pred,
            'sarima_prediction': sarima_pred,
            'ensemble_prediction': float(ensemble)
        }
    
    def _predict_future(self, target_date):
        """Predict for future date"""
        
        last_date = self.historical_data.index[-1]
        days_ahead = (target_date - last_date).days
        
        # Prophet
        future = self.prophet_model.make_future_dataframe(periods=days_ahead)
        prophet_forecast = self.prophet_model.predict(future)
        prophet_row = prophet_forecast[prophet_forecast['ds'] == target_date].iloc[0]
        
        # SARIMA
        sarima_forecast = self.sarima_model.get_forecast(steps=days_ahead)
        sarima_pred = float(sarima_forecast.predicted_mean.iloc[-1])
        sarima_ci = sarima_forecast.conf_int().iloc[-1]
        
        # Ensemble
        prophet_pred = float(prophet_row['yhat'])
        ensemble = (self.weight_prophet * prophet_pred) + (self.weight_sarima * sarima_pred)
        
        ensemble_lower = (self.weight_prophet * prophet_row['yhat_lower']) + (self.weight_sarima * sarima_ci.iloc[0])
        ensemble_upper = (self.weight_prophet * prophet_row['yhat_upper']) + (self.weight_sarima * sarima_ci.iloc[1])
        
        return {
            'date': target_date.strftime('%Y-%m-%d'),
            'type': 'future',
            'actual_sales': None,
            'prophet_prediction': prophet_pred,
            'sarima_prediction': sarima_pred,
            'ensemble_prediction': float(ensemble),
            'confidence_interval': {
                'lower': float(max(0, ensemble_lower)),
                'upper': float(ensemble_upper)
            }
        }
    
    def batch_predict(self, start_date: str, end_date: str) -> list:
        """Predict for date range"""
        
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        date_range = pd.date_range(start, end, freq='D')
        predictions = []
        
        for date in date_range:
            pred = self.predict(date.strftime('%Y-%m-%d'))
            predictions.append(pred)
        
        return predictions
    
    def next_week_forecast(self) -> dict:
        """Get next 7 days forecast"""
        
        last_date = self.historical_data.index[-1]
        predictions = []
        
        for i in range(1, 8):
            future_date = last_date + timedelta(days=i)
            pred = self.predict(future_date.strftime('%Y-%m-%d'))
            predictions.append(pred)
        
        avg_prediction = sum(p['ensemble_prediction'] for p in predictions) / len(predictions)
        
        return {
            'forecast_start': (last_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            'forecast_end': (last_date + timedelta(days=7)).strftime('%Y-%m-%d'),
            'average_daily_sales': round(avg_prediction, 2),
            'predictions': predictions
        }

forecast_service = ForecastService()