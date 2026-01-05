"""
Deal Risk Scoring System - XGBoost Classifier
"""
import pandas as pd
import numpy as np
import xgboost as xgb
from datetime import datetime
from typing import Dict, List, Optional
from app.config import settings

class DealRiskService:
    """
    Predicts Win/Loss probability for Salesforce Opportunities
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or (settings.MODEL_DIR / "deal_risk_model.json")
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load XGBoost model"""
        try:
            if self.model_path.exists():
                self.model = xgb.Booster()
                self.model.load_model(str(self.model_path))
            else:
                print(f"⚠️ Deal Risk Model not found at {self.model_path}. Using baseline logic.")
        except Exception as e:
            print(f"❌ Error loading Deal Risk Model: {e}")

    def engineer_features(self, opportunity: Dict) -> pd.DataFrame:
        """
        Engineers 15-20 attributes from SF Opportunity data
        """
        now = datetime.now()
        close_date = pd.to_datetime(opportunity.get('CloseDate'))
        created_date = pd.to_datetime(opportunity.get('CreatedDate'))
        
        # Core Features
        features = {
            'amount': float(opportunity.get('Amount', 0)),
            'days_open': (now - created_date).days,
            'days_to_close': (close_date - now).days,
            'probability': float(opportunity.get('Probability', 0)) / 100.0,
            'is_high_value': 1 if float(opportunity.get('Amount', 0)) > 100000 else 0,
        }
        
        # Derived Features
        features['deal_velocity'] = features['amount'] / max(1, features['days_open'])
        features['urgency_factor'] = 1.0 / max(1, features['days_to_close'])
        
        # Stage Encoding (Simple version)
        stages = ['Prospecting', 'Qualification', 'Needs Analysis', 'Proposal', 'Negotiation']
        current_stage = opportunity.get('StageName', 'Prospecting')
        for stage in stages:
            features[f'stage_{stage.lower().replace(" ", "_")}'] = 1 if current_stage == stage else 0
            
        # Activity Metrics (Mocking if not present)
        features['activity_score'] = float(opportunity.get('ActivityScore', 50)) / 100.0
        
        return pd.DataFrame([features])

    def predict_risk(self, opportunity: Dict) -> Dict:
        """
        Returns Win Probability and Risk Category
        """
        df = self.engineer_features(opportunity)
        
        if self.model:
            dmatrix = xgb.DMatrix(df)
            win_prob = float(self.model.predict(dmatrix)[0])
        else:
            # Baseline Scoring Logic (Feature Engineering based)
            win_prob = self._calculate_baseline_prob(df)
        
        # Categorize Risk
        if win_prob > 0.75:
            category = "LOW"
            priority = "LOW"
        elif win_prob > 0.50:
            category = "MEDIUM"
            priority = "MEDIUM"
        else:
            category = "HIGH"
            priority = "HIGH"
            
        return {
            "opportunity_id": opportunity.get('Id'),
            "win_probability": round(win_prob, 4),
            "risk_score": round((1 - win_prob) * 100, 2),
            "risk_category": category,
            "action_priority": priority,
            "key_factors": self._get_key_factors(df, win_prob)
        }

    def _calculate_baseline_prob(self, df: pd.DataFrame) -> float:
        """Heuristic-based probability when model is missing"""
        row = df.iloc[0]
        prob = row['probability'] * 0.5 # Start with SF probability weight
        
        # Adjustments
        if row['days_to_close'] < 7: prob -= 0.1
        if row['activity_score'] > 0.7: prob += 0.2
        if row['stage_negotiation'] == 1: prob += 0.1
        
        return float(np.clip(prob, 0.05, 0.95))

    def _get_key_factors(self, df: pd.DataFrame, prob: float) -> List[str]:
        row = df.iloc[0]
        factors = []
        if row['days_to_close'] < 14: factors.append("Close date approaching")
        if row['amount'] > 100000: factors.append("High-value deal")
        if row['activity_score'] < 0.3: factors.append("Low interaction activity")
        if prob < 0.5: factors.append("Below historical win threshold for stage")
        return factors

deal_risk_service = DealRiskService()
