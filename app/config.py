"""
Configuration and settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE = "Retail Sales Forecasting API"
    API_VERSION = "1.0.0"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # LLM & API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#sales-alerts")
    
    # Salesforce
    SF_USERNAME = os.getenv("SF_USERNAME")
    SF_PASSWORD = os.getenv("SF_PASSWORD")
    SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")
    SF_DOMAIN = os.getenv("SF_DOMAIN", "login")
    
    # Gmail
    GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    
    # Model Paths
    BASE_DIR = Path(__file__).parent.parent
    MODEL_DIR = BASE_DIR / "models"
    
    PROPHET_MODEL_PATH = MODEL_DIR / "prophet_model.pkl"
    SARIMA_MODEL_PATH = MODEL_DIR / "sarima_model.pkl"
    ANOMALY_MODEL_PATH = MODEL_DIR / "anomaly_detector.pkl"
    ENSEMBLE_CONFIG_PATH = MODEL_DIR / "ensemble_config.pkl"
    RISK_CONFIG_PATH = MODEL_DIR / "risk_config.pkl"
    HISTORICAL_DATA_PATH = MODEL_DIR / "historical_sales.csv"
    
    # Ensemble Weights
    WEIGHT_PROPHET = 0.4
    WEIGHT_SARIMA = 0.6

settings = Settings()