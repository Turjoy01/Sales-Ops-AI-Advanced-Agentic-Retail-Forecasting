# Sales Ops AI: Advanced Agentic Retail Forecasting �

**Sales Ops AI** is an enterprise-grade, agentic retail forecasting system designed to bridge the gap between raw data and executive decision-making. Built with **FastAPI**, it leverages state-of-the-art **ML Ensembles**, **XGBoost classifiers**, and **Generative AI** to deliver not just predictions, but autonomous business actions.

---

## 🧠 The Agentic Core: Why "Agentic"?

Unlike traditional dashboards that merely display data, this system is an **Active Agent** that:
1.  **Evaluates Decisions**: Automatically triggers workflows (Email alerts, Salesforce tasks) based on forecast reliability and risk thresholds.
2.  **Analyzes Deal Risks**: Predicts Win/Loss probabilities for Salesforce opportunities using a custom-trained **XGBoost model**.
3.  **Closes the Loop**: Synchronizes directly with **Salesforce** to update opportunities and create follow-up tasks for Sales teams.

---

## 🌟 Key Features

### 1. 📈 Intelligent Forecasting Engine
- **Weighted ML Ensemble**: Combines **Meta Prophet** (trend/seasonality) and **SARIMA** (stochastic patterns) for balanced accuracy.
- **Dynamic Date Range**: Generate predictions for any future date range with real-time model interpolation.
- **Deep Volatility Audit**: Every forecast includes a risk-weighted confidence score based on historical Coefficient of Variation (CV).

### 2. 🛡️ Risk & Anomaly Intelligence
- **Isolation Forest Detection**: Automatically flags "Black Swan" events and data outliers in historical sales.
- **Trend Deviation Safeguard**: Detects when forecasts drift too far from moving averages to prevent over-projection.
- **Win Probability Scoring**: Advanced feature engineering (velocity, urgency, activity score) to predict CRM deal outcomes.

### 3. 🔌 Enterprise Integrations
- **Salesforce CRM**: Bidirectional sync of opportunities, historical data, and task creation.
- **Google Sheets**: Live importing of retail targets and budget data.
- **Communications**: Automated Slack notifications and Weekly Email Reports via `aiosmtplib`.

### 4. 🎨 Premium Analytics Dashboard
- **Glassmorphism UI**: A state-of-the-art, responsive white-and-green aesthetic designed for clarity and speed.
- **Pro-Grade PDF Export**: High-contrast, blur-free report generation for executive meetings.
- **AI Narrative Insights**: Powered by GPT-4o to translate complex model weights into actionable business strategies.

---

## 📁 Project Architecture

```bash
retail-forecasting-system/
├── app/
│   ├── api/               # FastAPI Routers (Forecast, Risk, Integrations, etc.)
│   ├── services/          # Agent Logic (Decision Engine, Deal Risk, Salesforce)
│   ├── models/            # ML Logic (Prophet, SARIMA, XGBoost, Anomaly Detectors)
│   └── config.py          # Unified system configuration
├── frontend/              # Modern SPA Dashboard
│   ├── static/js/         # Modular API Client & Page Controllers
│   └── pages/             # Responsive HTML Viewports
├── main.py                # System Entry Point
└── .env                   # Security & Integration Credentials
```

---

## 🛠️ Getting Started

### 1. Installation
```bash
# Clone and setup environment
python -m venv .venv
source .venv/bin/activate  # or .\ .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file with your credentials:
```env
# AI & Analytics
OPENAI_API_KEY=sk_...
# CRM & Integrations
SF_USERNAME=your_sf_user
SF_PASSWORD=your_sf_pass
SF_SECURITY_TOKEN=your_token
# Communications
GMAIL_ADDRESS=...
GMAIL_APP_PASSWORD=...
```

### 3. Launch the Agent
```bash
uvicorn main:app --reload
```
Navigate to `http://localhost:8000` to access the dashboard.

---

## 📡 API Capabilities

| Category | Endpoint | Action |
| :--- | :--- | :--- |
| **Forecasting** | `POST /api/v1/forecast/predict` | Deep prediction for specific date |
| **Risk** | `GET /api/v1/risk/analysis` | Dynamic historical & future risk audit |
| **Salesforce** | `POST /api/v1/integrations/sf/sync` | Force bidirectional data sync |
| **Decisions** | `POST /api/v1/decisions/evaluate` | Trigger agentic rule-based actions |
| **System** | `GET /health` | Real-time ML model heartbeat check |

---
*Developed with Advanced Agentic Workflows for the Future of Retail.*

