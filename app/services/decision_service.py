"""
Decision Service - Rules Engine
"""
from typing import List, Dict

class DecisionService:
    """
    Evaluates forecasts and risks to determine necessary actions.
    """

    def evaluate(self, forecast_value: float, risk_data: dict) -> Dict:
        """
        Evaluate rules and return actions.
        """
        actions = []
        risk_score = risk_data.get('risk_score', 0)
        reliability = risk_data.get('reliability', 'MEDIUM')
        
        # Rule 1: High Risk & Low Reliability -> Alert + Task
        if risk_score >= 70 and reliability == "LOW":
            actions.append("SEND_EMAIL_ALERT")
            actions.append("CREATE_SALESFORCE_TASK")
            priority = "HIGH"
            reason = "High risk with low reliability"
            
        # Rule 2: High Risk but High Reliability -> Just Alert
        elif risk_score >= 70:
            actions.append("SEND_EMAIL_ALERT")
            priority = "MEDIUM"
            reason = "High risk detected"
            
        # Rule 3: Anomaly Detected -> Flag
        elif risk_data.get('is_anomaly', False):
            actions.append("FLAG_FOR_REVIEW")
            actions.append("INCLUDE_IN_WEEKLY_REPORT")
            priority = "MEDIUM"
            reason = "Anomaly detected"

        # Rule 4: Critical Drop (Mock threshold)
        elif forecast_value < 2000: # Example threshold
             actions.append("INVENTORY_WARNING")
             priority = "HIGH"
             reason = "Forecast below critical threshold"

        else:
            actions.append("LOG_ONLY")
            priority = "LOW"
            reason = "Normal forecast"

        return {
            "actions": actions,
            "priority": priority,
            "reason": reason
        }

decision_service = DecisionService()
