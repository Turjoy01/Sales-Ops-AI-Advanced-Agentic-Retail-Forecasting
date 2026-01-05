"""
Basic API tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_forecast_predict():
    """Test single forecast prediction"""
    # Using a historical date to avoid actual model logic complexities in tests if possible
    # but the service handles both.
    response = client.post(
        "/api/v1/forecast/predict",
        json={"date": "2018-01-01"}
    )
    assert response.status_code == 200
    assert "ensemble_prediction" in response.json()

def test_risk_analysis():
    """Test risk analysis endpoint"""
    response = client.get("/api/v1/risk/analysis")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_models_info():
    """Test models info endpoint"""
    response = client.get("/api/v1/models/info")
    assert response.status_code == 200
    assert "model_version" in response.json()
