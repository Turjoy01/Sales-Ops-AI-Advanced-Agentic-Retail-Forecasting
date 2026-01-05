import { api } from './api.js';

class RiskController {
    constructor() {
        this.filterBtn = document.getElementById('applyFiltersBtn');
        this.startDate = document.getElementById('riskStartDate');
        this.endDate = document.getElementById('riskEndDate');
        this.levelFilter = document.getElementById('riskLevelFilter');
        this.tableBody = document.querySelector('#riskTable tbody');
        this.pieChart = document.getElementById('riskPieChart');

        this.init();
    }

    init() {
        if (this.filterBtn) {
            this.filterBtn.addEventListener('click', () => this.loadData());
        }
        // Load initial data
        this.loadData();
    }

    async loadData() {
        const btn = this.filterBtn;
        if (btn) btn.innerHTML = '<div class="spinner"></div> Loading...';

        try {
            const level = this.levelFilter.value;
            const start = this.startDate.value;
            const end = this.endDate.value;

            console.log(`Requesting risk analysis... Range: ${start || 'all'} to ${end || 'all'}, Level: ${level}`);

            // Fetch data with filters passed to backend
            const data = await api.getRiskAnalysis(start, end);
            let reports = Array.isArray(data) ? data : (data.detailed_reports || []);

            // Still apply level filter client-side for now as backend doesn't handle it yet
            if (level !== 'ALL') {
                reports = reports.filter(r => (r.risk_level || '').toUpperCase() === level.toUpperCase());
            }

            this.renderTable(reports);
            this.renderStats(reports);

            if (btn) btn.innerHTML = '<i class="fas fa-filter"></i> Apply Filters';
        } catch (error) {
            console.error(error);
            // Don't show mock data if API is actually returning empty range
            this.tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error loading data. Please try again.</td></tr>';
            if (btn) btn.innerHTML = '<i class="fas fa-filter"></i> Apply Filters';
        }
    }

    renderTable(rows) {
        if (!rows || rows.length === 0) {
            this.tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No records found</td></tr>';
            const info = document.getElementById('tablePaginationInfo');
            if (info) info.innerText = 'Showing 0 records';
            return;
        }

        const info = document.getElementById('tablePaginationInfo');
        if (info) info.innerText = `Showing all ${rows.length} records (Filtered)`;

        this.tableBody.innerHTML = rows.map(row => `
            <tr>
                <td>${row.date}</td>
                <td class="font-bold">$${Math.round(row.forecast_value || row.forecast || 0)}</td>
                <td>${row.risk_score}</td>
                <td><span class="badge ${this.getBadgeClass(row.risk_level)}">${row.risk_level}</span></td>
                <td>${this.getStatusIcon(row.risk_level)}</td>
                <td><button class="btn btn-secondary" style="padding: 4px 8px;" onclick="alert('Risk Score: ${row.risk_score}\\nFactors: ${row.risk_factors || 'None'}')">Details</button></td>
            </tr>
        `).join('');
    }

    renderStats(rows) {
        const total = rows.length;
        if (total === 0) {
            this.pieChart.innerHTML = "No Data";
            return;
        }
        const high = rows.filter(r => (r.risk_level || '').toUpperCase() === 'HIGH').length;
        const medium = rows.filter(r => (r.risk_level || '').toUpperCase() === 'MEDIUM').length;
        const low = rows.filter(r => (r.risk_level || '').toUpperCase() === 'LOW').length;

        this.pieChart.innerHTML = `
            <div style="text-align:center; display: flex; justify-content: center; gap: 20px; align-items: center; height: 100%;">
                <span class="text-danger font-bold">High: ${Math.round(high / total * 100)}%</span>
                <span class="text-warning font-bold">Medium: ${Math.round(medium / total * 100)}%</span>
                <span class="text-success font-bold">Low: ${Math.round(low / total * 100)}%</span>
            </div>
        `;
    }

    getBadgeClass(level) {
        const l = (level || '').toUpperCase();
        if (l === 'HIGH') return 'badge-danger';
        if (l === 'MEDIUM') return 'badge-warning';
        return 'badge-success';
    }

    getStatusIcon(level) {
        const l = (level || '').toUpperCase();
        if (l === 'HIGH') return '<i class="fas fa-exclamation-triangle text-danger"></i> Anomaly';
        if (l === 'MEDIUM') return '<i class="fas fa-exclamation-circle text-warning"></i> Warning';
        return '<i class="fas fa-check text-success"></i> Normal';
    }

    getMockData() {
        return [
            { date: '2025-01-10', forecast: 2900, risk_score: 85, risk_level: 'HIGH', explanation: 'Sudden Drop' },
            { date: '2025-01-11', forecast: 3100, risk_score: 45, risk_level: 'MEDIUM', explanation: 'Volatility' },
            { date: '2025-01-12', forecast: 3300, risk_score: 12, risk_level: 'LOW', explanation: 'Stable' }
        ];
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new RiskController();
});
