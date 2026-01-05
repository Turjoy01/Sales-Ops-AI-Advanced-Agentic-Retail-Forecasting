"""
Email Service - Gmail Alerts
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailService:
    """Email alert service"""
    
    def __init__(self):
        self.sender = settings.GMAIL_ADDRESS
        self.password = settings.GMAIL_APP_PASSWORD.replace(" ", "") if settings.GMAIL_APP_PASSWORD else ""
    
    def send_report(self, report: dict, recipient: str = None) -> bool:
        """
        Send forecast report via email
        
        Args:
            report: Report dict
            recipient: Recipient email (default: self)
        
        Returns:
            bool: Success status
        """
        
        if recipient is None:
            recipient = self.sender
        
        forecast = report['forecast']
        risk = report['risk']
        explanation = report['explanation']
        
        # Build HTML email
        color_map = {'Low': '#4CAF50', 'Medium': '#FF9800', 'High': '#F44336'}
        risk_level = risk.get('risk_level', 'Medium')
        risk_color = color_map.get(risk_level, '#2196F3')
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #2196F3;">📊 Sales Forecast Report</h2>
    
    <div style="background: #f5f5f5; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3;">
        <h3>🔮 Prediction for {forecast['date']}</h3>
        <p><strong>Expected Sales:</strong> ${forecast['ensemble_prediction']:,.2f}</p>
        <p style="font-size: 14px; color: #666;">
            Prophet: ${forecast['prophet_prediction']:,.2f} | 
            SARIMA: ${forecast.get('sarima_prediction', 0):,.2f}
        </p>
    </div>
    
    <div style="background: {risk_color}20; padding: 15px; margin: 10px 0; border-left: 4px solid {risk_color};">
        <h3>⚠️ Risk Assessment</h3>
        <p><strong>Risk Level:</strong> <span style="color: {risk_color}; font-weight: bold;">{risk['risk_level']}</span> ({risk['risk_score']}/100)</p>
        <p><strong>Reliability:</strong> {risk['reliability']}</p>
        <p><strong>Deviation:</strong> {risk['deviation_from_mean']:+.1f}% from average</p>
        {'<p><strong>Factors:</strong><br>' + '<br>'.join('• ' + f for f in risk['risk_factors']) + '</p>' if risk['risk_factors'] else ''}
    </div>
    
    <div style="background: #e3f2fd; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3;">
        <h3>🤖 AI Analysis</h3>
        <p style="white-space: pre-line;">{explanation}</p>
    </div>
    
    <hr style="margin: 20px 0;">
    <p style="color: #999; font-size: 12px;">
        Generated: {report['generated_at']}<br>
        System: Retail Sales Forecasting API v1.0
    </p>
</body>
</html>
"""
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender
            msg['To'] = recipient
            msg['Subject'] = f"Sales Forecast Alert - {forecast['date']}"
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send via Gmail
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {recipient}")
            return True
        
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False

email_service = EmailService()