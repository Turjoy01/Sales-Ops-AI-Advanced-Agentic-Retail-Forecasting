import { api } from './api.js';

class ForecastController {
    constructor() {
        // Elements must use IDs now
        this.dateInput = document.getElementById('forecastDateInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.downloadBtn = document.getElementById('downloadReportBtn');
        this.alertBtn = document.getElementById('sendAlertBtn');

        // Output Elements
        this.predictedSales = document.getElementById('predictedSales');
        this.confidenceRange = document.getElementById('confidenceRange');
        this.modelConfidence = document.getElementById('modelConfidence');
        this.prophetValue = document.getElementById('prophetValue');
        this.sarimaValue = document.getElementById('sarimaValue');

        this.riskLevelDisplay = document.getElementById('riskLevelDisplay');
        this.riskScoreDisplay = document.getElementById('riskScoreDisplay');
        this.anomalyBadge = document.getElementById('anomalyBadge');
        this.reliabilityBadge = document.getElementById('reliabilityBadge');

        this.aiExplanation = document.getElementById('aiExplanation');
        this.aiRecommendation = document.getElementById('aiRecommendation');

        this.init();
    }

    init() {
        // Set default date to tomorrow
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        try {
            this.dateInput.valueAsDate = tomorrow;
        } catch (e) { }

        // Bind Events
        if (this.analyzeBtn) this.analyzeBtn.addEventListener('click', () => this.handleAnalyze());
        if (this.downloadBtn) this.downloadBtn.addEventListener('click', () => this.handleDownload());
        if (this.alertBtn) this.alertBtn.addEventListener('click', () => this.handleAlert());
    }

    async handleAnalyze() {
        const date = this.dateInput.value;
        if (!date) {
            alert('Please select a date first.');
            return;
        }

        const btn = this.analyzeBtn;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<div class="spinner"></div> Processing...';
        btn.disabled = true;

        try {
            // Retrieve full report which includes forecast, risk, and AI explanation
            const fullReport = await api.generateReport({ date: date, send_email: false });
            this.updateUI(fullReport);

            btn.innerHTML = '<i class="fas fa-check"></i> Done';
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 1000);

        } catch (error) {
            console.error(error);
            alert('Analysis failed: ' + error.message);
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    updateUI(report) {
        const { forecast, risk, explanation } = report;

        // --- Forecast ---
        this.predictedSales.textContent = `$${Math.round(forecast.ensemble_prediction).toLocaleString()}`;
        this.confidenceRange.textContent = `$${Math.round(forecast.lower_bound).toLocaleString()} - $${Math.round(forecast.upper_bound).toLocaleString()}`;
        this.modelConfidence.textContent = `${Math.round(forecast.confidence_score * 100)}% CONFIDENCE`;

        // Model breakdown (assuming mock breakdown in schema if not present)
        const prophetVal = forecast.model_breakdown?.prophet || forecast.ensemble_prediction * 0.95;
        const sarimaVal = forecast.model_breakdown?.sarima || forecast.ensemble_prediction * 1.05;
        this.prophetValue.textContent = `$${Math.round(prophetVal).toLocaleString()}`;
        this.sarimaValue.textContent = `$${Math.round(sarimaVal).toLocaleString()}`;

        // --- Risk ---
        this.riskLevelDisplay.textContent = `${risk.risk_level.toUpperCase()}`;
        this.riskScoreDisplay.textContent = `Score: ${risk.risk_score}/100`;
        this.riskLevelDisplay.className = `text-xl font-bold ${this.getColorClass(risk.risk_level)}`;

        // Badges
        this.anomalyBadge.textContent = risk.is_anomaly ? 'ANOMALY DETECTED' : 'Normal';
        this.anomalyBadge.className = `badge ${risk.is_anomaly ? 'badge-danger' : 'badge-success'}`;

        this.reliabilityBadge.textContent = risk.reliability;
        this.reliabilityBadge.className = `badge ${risk.reliability === 'HIGH' ? 'badge-success' : 'badge-warning'}`;

        // --- AI ---
        // Basic parsing of explanation or just raw dump
        this.aiExplanation.innerHTML = explanation.replace(/\n/g, '<br>');
        this.aiRecommendation.style.display = 'block';
        this.aiRecommendation.innerHTML = `<strong>Recommendation:</strong> Based on risk level ${risk.risk_level}, check inventory and staff levels.`;
    }

    getColorClass(level) {
        if (level === 'HIGH') return 'text-danger';
        if (level === 'MEDIUM') return 'text-warning';
        return 'text-success';
    }

    async handleDownload() {
        const date = this.dateInput.value;
        const btn = this.downloadBtn;
        btn.innerHTML = '<div class="spinner"></div>';
        setTimeout(() => {
            alert(`PDF Report for ${date} downloaded! (Mock)`);
            btn.innerHTML = 'Download Report';
        }, 1500);
    }

    async handleAlert() {
        const btn = this.alertBtn;
        btn.innerHTML = '<div class="spinner"></div>';
        try {
            await api.emailReport({
                date: this.dateInput.value,
                send_email: true,
                recipient_email: "team@company.com" // Default or fetched
            });
            alert("Alert sent to team successfully!");
        } catch (e) {
            alert("Failed to send alert.");
        } finally {
            btn.innerHTML = 'Send Alert to Team';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ForecastController();
});
