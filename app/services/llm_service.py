"""
LLM Service - OpenAI & Anthropic Claude
"""
import openai
import anthropic
from typing import Dict, Optional
from app.config import settings

class LLMService:
    """LLM explanation and insights service"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_explanation(self, forecast: dict, risk: dict) -> str:
        """Generate explanation using OpenAI or Anthropic"""
        
        prompt = f"""
You are a sales analyst. Explain this forecast concisely:

**Forecast:**
- Date: {forecast['date']}
- Predicted: ${forecast['ensemble_prediction']:,.2f}

**Risk:**
- Level: {risk['risk_level']} ({risk['risk_score']}/100)
- Reliability: {risk['reliability']}
- Deviation: {risk.get('deviation_from_mean', 0):.1f}%

Provide:
1. Brief summary (1-2 sentences)
2. Risk explanation
3. 3 actionable recommendations
"""
        return self._call_llm(prompt, system_prompt="You are a sales forecasting expert.")

    def generate_deal_insights(self, opportunity: Dict, risk_data: Dict) -> str:
        """
        Feature 3: AI Deal Insights Generator
        Generates analysis + recommendations + email template
        """
        prompt = f"""
Analyze this Salesforce Opportunity and provide strategic insights:

**Deal Info:**
- Name: {opportunity.get('Name')}
- Amount: ${opportunity.get('Amount', 0):,.2f}
- Stage: {opportunity.get('StageName')}
- Close Date: {opportunity.get('CloseDate')}

**AI Risk Assessment:**
- Win Probability: {risk_data['win_probability']*100:.1f}%
- Risk Category: {risk_data['risk_category']}
- Risk Factors: {', '.join(risk_data['key_factors'])}

Please provide:
1. **Executive Summary**: 2-3 paragraphs on deal health.
2. **Action Recommendations**: 3-5 bullet points for the sales rep.
3. **Outreach Email Draft**: A personalized email template for the customer.
4. **Competitive Strategy**: Advice on positioning.
"""
        return self._call_llm(prompt, system_prompt="You are a senior sales strategist and Claude Sonnet 4 expert.")

    def _call_llm(self, prompt: str, system_prompt: str) -> str:
        """Helper to call available LLM (Prefers Anthropic)"""
        
        # Anthropic (Claude)
        if self.anthropic_client:
            try:
                message = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            except Exception as e:
                print(f"⚠️ Anthropic API error: {e}")

        # OpenAI (GPT)
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"⚠️ OpenAI API error: {e}")

        return "LLM Service unavailable. Please check API keys."

llm_service = LLMService()
