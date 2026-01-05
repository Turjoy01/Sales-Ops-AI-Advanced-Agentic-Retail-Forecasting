"""
Automation Service - Orchestrates the Sales Intelligence Agent Pipeline
"""
from app.services.salesforce_service import salesforce_service
from app.services.deal_risk_service import deal_risk_service
from app.services.llm_service import llm_service
from app.services.slack_service import slack_service
from typing import Dict, List

class AutomationService:
    """
    Feature 4 & 5: Executes automated actions based on logic rules
    """
    
    async def run_daily_pipeline(self) -> Dict:
        """
        Executes the full agent pipeline:
        1. Sync Opportunities
        2. Score Risk
        3. Generate Insights
        4. Update SF Fields
        5. Create Tasks (if needed)
        6. Send Notifications
        """
        print("🚀 Starting Daily Sales Intelligence Pipeline...")
        
        opportunities = salesforce_service.get_open_opportunities()
        results = {
            "processed": 0,
            "tasks_created": 0,
            "alerts_sent": 0,
            "errors": 0
        }
        
        for opp in opportunities:
            try:
                # 1. Score Risk
                risk_data = deal_risk_service.predict_risk(opp)
                
                # 2. Update Salesforce Fields (Feature 6)
                sf_update = {
                    "AI_Risk_Score__c": risk_data['risk_score'],
                    "Risk_Category__c": risk_data['risk_category']
                }
                salesforce_service.update_opportunity(opp['Id'], sf_update)
                
                # 3. Decision Logic for Heavy Actions (Feature 4)
                if risk_data['risk_category'] == "HIGH" or risk_data['win_probability'] < 0.5:
                    
                    # Generate Insights (Feature 3)
                    insights = llm_service.generate_deal_insights(opp, risk_data)
                    
                    # Create Task (Feature 4)
                    task_data = {
                        "Subject": f"High Risk Follow-up: {opp['Name']}",
                        "Description": insights,
                        "WhatId": opp['Id'],
                        "Priority": "High",
                        "Status": "Not Started"
                    }
                    salesforce_service.create_task(task_data)
                    results["tasks_created"] += 1
                    
                    # Send Slack Alert (Feature 5)
                    insights_link = f"https://force.com/{opp['Id']}" # In real app, links to dashboard
                    slack_service.send_deal_alert(opp, risk_data, insights_link)
                    results["alerts_sent"] += 1
                
                results["processed"] += 1
                
            except Exception as e:
                print(f"❌ Error processing opportunity {opp.get('Id')}: {e}")
                results["errors"] += 1
                
        print(f"✅ Pipeline Completed: {results}")
        return results

automation_service = AutomationService()
