"""
Slack Notification Service
"""
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, Optional
from app.config import settings

class SlackService:
    """
    Feature 5: Slack/Email Alert System
    Handles Slack messaging and block-formatted alerts
    """
    
    def __init__(self):
        self.client = None
        if settings.SLACK_BOT_TOKEN:
            self.client = WebClient(token=settings.SLACK_BOT_TOKEN)
        else:
            print("⚠️ Slack Bot Token missing. Slack service disabled.")

    def send_alert(self, title: str, message: str, color: str = "#36a64f", channel: Optional[str] = None) -> bool:
        """Send a basic rich alert to Slack"""
        if not self.client:
            print(f"Mock Slack Alert: [{title}] {message}")
            return True
            
        target_channel = channel or settings.SLACK_CHANNEL
        
        try:
            attachment = {
                "color": color,
                "title": title,
                "text": message,
                "footer": "SalesOps AI Agent"
            }
            self.client.chat_postMessage(
                channel=target_channel,
                attachments=[attachment]
            )
            return True
        except SlackApiError as e:
            print(f"❌ Slack Error: {e.response['error']}")
            return False

    def send_deal_alert(self, opportunity: Dict, risk_data: Dict, insights_link: str):
        """
        Specific high-risk deal alert with interactive blocks
        """
        title = "🚨 High-Risk Deal Alert"
        message = (
            f"*Deal:* {opportunity.get('Name')}\n"
            f"*Amount:* ${opportunity.get('Amount', 0):,.2f}\n"
            f"*Win Probability:* {risk_data['win_probability']*100:.1f}%\n"
            f"*Owner:* {opportunity.get('OwnerId')}\n\n"
            f"<{insights_link}|View Deal & Recommendations>"
        )
        
        color = "#ff0000" if risk_data['risk_category'] == "HIGH" else "#ff9900"
        return self.send_alert(title, message, color=color)

slack_service = SlackService()
