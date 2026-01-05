"""
ML Model Loader - Load models once at startup
"""
import pickle
import pandas as pd
from app.config import settings

class ModelLoader:
    """Singleton class to load and store ML models"""
    
    _instance = None
    _models_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._models_loaded:
            self.load_models()
    
    def load_models(self):
        """Load all ML models"""
        try:
            # Prophet Model
            with open(settings.PROPHET_MODEL_PATH, 'rb') as f:
                self.prophet_model = pickle.load(f)
            
            # SARIMA Model
            with open(settings.SARIMA_MODEL_PATH, 'rb') as f:
                self.sarima_model = pickle.load(f)
            
            # Anomaly Detector
            with open(settings.ANOMALY_MODEL_PATH, 'rb') as f:
                self.anomaly_detector = pickle.load(f)
            
            # Ensemble Config
            with open(settings.ENSEMBLE_CONFIG_PATH, 'rb') as f:
                self.ensemble_config = pickle.load(f)
            
            # Risk Config
            with open(settings.RISK_CONFIG_PATH, 'rb') as f:
                self.risk_config = pickle.load(f)
            
            # Historical Data
            self.historical_data = pd.read_csv(
                settings.HISTORICAL_DATA_PATH,
                index_col=0,
                parse_dates=True
            )
            
            self._models_loaded = True
            print("✅ All models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def get_prophet(self):
        return self.prophet_model
    
    def get_sarima(self):
        return self.sarima_model
    
    def get_anomaly_detector(self):
        return self.anomaly_detector
    
    def get_historical_data(self):
        return self.historical_data
    
    def get_config(self):
        return self.ensemble_config, self.risk_config

# Global instance
model_loader = ModelLoader()