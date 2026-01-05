import { api } from './api.js';

class DashboardController {
    constructor() {
        this.todayEl = document.getElementById('todayForecast');
        this.chartCanvas = document.getElementById('mainChart');
        this.exportBtn = document.querySelector('button.btn-secondary'); // "Export PDF"
        this.chartInstance = null;

        this.init();
    }

    async init() {
        console.log('Initializing Dashboard with Chart.js...');

        // Export Button
        if (this.exportBtn) {
            this.exportBtn.addEventListener('click', () => this.handleExport());
        }

        try {
            // Load Forecast Data (Next Week includes today/tomorrow)
            const forecastData = await api.getNextWeekForecast();
            this.renderForecasts(forecastData);

            // Load Risk Data
            const riskData = await api.getRiskAnalysis();
            this.renderRisk(riskData);

        } catch (error) {
            console.error('Dashboard Load Error:', error);
            // Handling error state on canvas parent if needed
        }
    }

    async handleExport() {
        const btn = this.exportBtn;
        const dashboardElement = document.querySelector('.dashboard-content');
        const originalText = btn.innerHTML;

        btn.innerHTML = '<div class="spinner"></div> Generating PDF...';
        btn.disabled = true;

        // --- 1. FORCE LIGHT MODE FOR PDF ---
        // We use a temporary style tag to override ALL dark themes
        const styleId = 'pdf-export-styles';
        let style = document.getElementById(styleId);
        if (!style) {
            style = document.createElement('style');
            style.id = styleId;
            document.head.appendChild(style);
        }

        // Critical: Set background to white and text to black
        style.innerHTML = `
            /* Container reset */
            .dashboard-content {
                background: #ffffff !important;
                padding: 1rem !important;
            }
            /* Universal clear styles */
            .dashboard-content, .dashboard-content * {
                background-image: none !important;
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
                filter: none !important;
                box-shadow: none !important;
                text-shadow: none !important;
                color: #111827 !important; /* Extremely dark gray/black */
            }
            /* Card & Layout clarity */
            .glass-card {
                background: #ffffff !important;
                border: 2px solid #e5e7eb !important;
                border-radius: 12px !important;
                margin-bottom: 1.5rem !important;
            }
            .metric-value {
                color: #000000 !important;
                font-weight: 800 !important;
                font-size: 2.5rem !important;
            }
            .text-muted {
                color: #4b5563 !important;
                font-weight: 500 !important;
            }
            h1, h2, h3, h4, h5 {
                color: #111827 !important;
                font-weight: 700 !important;
            }
            /* Badge handling for contrast */
            .badge {
                border: 1px solid #d1d5db !important;
                background: #f3f4f6 !important;
            }
            .badge-success { color: #065f46 !important; }
            .badge-warning { color: #92400e !important; }
            .badge-danger { color: #991b1b !important; }
            
            /* Chart spacing */
            .chart-container {
                background: #f9fafb !important;
                border: 1px solid #e5e7eb !important;
                margin-top: 1rem !important;
            }
        `;

        // --- 2. UPDATE CHART AXIS COLORS ---
        if (this.chartInstance) {
            // Switch to dark axis lines/text for white background
            this.chartInstance.options.scales.x.ticks.color = '#000000';
            this.chartInstance.options.scales.x.ticks.font = { weight: 'bold', size: 12 };
            this.chartInstance.options.scales.y.ticks.color = '#000000';
            this.chartInstance.options.scales.y.ticks.font = { weight: 'bold', size: 12 };
            this.chartInstance.options.scales.y.grid.color = 'rgba(0,0,0,0.2)';
            this.chartInstance.update();
        }

        // --- 3. WAIT FOR RENDERING ---
        await new Promise(r => setTimeout(r, 800)); // Allow DOM/Canvas to repaint

        const opt = {
            margin: 0.25,
            filename: `sales_ops_report_${new Date().toISOString().slice(0, 10)}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2, useCORS: true, logging: false },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'landscape' }
        };

        try {
            await html2pdf().set(opt).from(dashboardElement).save();
        } catch (err) {
            console.error("PDF Export failed", err);
            alert("Export failed: " + err.message);
        } finally {
            // --- 4. CLEANUP (Revert to Dark Mode) ---
            style.remove(); // Remove overrides

            if (this.chartInstance) {
                // Revert chart to dark mode colors
                this.chartInstance.options.scales.x.ticks.color = '#94a3b8';
                this.chartInstance.options.scales.y.ticks.color = '#94a3b8';
                this.chartInstance.options.scales.y.grid.color = 'rgba(255, 255, 255, 0.05)';
                this.chartInstance.update();
            }

            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    renderForecasts(data) {
        if (!data || !data.predictions || data.predictions.length === 0) return;

        const predictions = data.predictions;
        const labels = predictions.map(d => d.date);
        const values = predictions.map(d => Math.round(d.ensemble_prediction));

        // Destroy existing chart if any
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        const ctx = this.chartCanvas.getContext('2d');

        // Create Gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.5)');
        gradient.addColorStop(1, 'rgba(99, 102, 241, 0.0)');

        this.chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales Forecast ($)',
                    data: values,
                    borderColor: '#6366f1', // Primary brand color
                    backgroundColor: gradient,
                    borderWidth: 3,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#6366f1',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#94a3b8',
                            callback: function (value) {
                                return '$' + value;
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    }
                }
            }
        });

        // Update Text Metrics (Today/Tomorrow)
        const today = predictions[0];
        const tomorrow = predictions[1];

        const todayVal = document.querySelector('.glass-card:nth-child(1) .metric-value');
        if (todayVal && today) todayVal.innerText = `$${Math.round(today.ensemble_prediction).toLocaleString()}`;

        const tmrwVal = document.querySelector('.glass-card:nth-child(2) .metric-value');
        if (tmrwVal && tomorrow) tmrwVal.innerText = `$${Math.round(tomorrow.ensemble_prediction).toLocaleString()}`;
    }

    renderRisk(data) {
        // Logic to render risk meter...
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new DashboardController();
});
