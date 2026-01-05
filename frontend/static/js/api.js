/**
 * API Client for Sales Ops AI
 * Handles communication with backend endpoints
 */

const API_BASE = '/api/v1';

class ApiClient {
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`);
            if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error('GET Error:', error);
            throw error;
        }
    }

    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error('POST Error:', error);
            throw error;
        }
    }

    // --- Endpoints ---

    // Forecasts
    async getNextWeekForecast() {
        return this.get('/forecast/next-week');
    }

    async predictDate(date) {
        return this.post('/forecast/predict', { date });
    }

    // Risk
    async getRiskAnalysis(startDate = '', endDate = '') {
        const query = (startDate || endDate) ? `?start_date=${startDate}&end_date=${endDate}` : '';
        return this.get(`/risk/analysis${query}`);
    }

    // Decisions
    async evaluateDecision(data) {
        return this.post('/decisions/evaluate', data);
    }

    // Integrations
    async toggleSalesforceSync(dates) {
        return this.post('/integrations/salesforce/sync', dates);
    }

    async createSalesforceTask(taskUrl) {
        return this.post('/integrations/salesforce/create-task', taskUrl);
    }

    // Reports
    async generateReport(data) {
        return this.post('/reports/generate', data);
    }

    async emailReport(data) {
        return this.post('/reports/email', data);
    }

    async getWeeklyReport() {
        return this.get('/reports/weekly');
    }

    async checkHealth() {
        return fetch('/health').then(res => res.json());
    }
}

export const api = new ApiClient();
