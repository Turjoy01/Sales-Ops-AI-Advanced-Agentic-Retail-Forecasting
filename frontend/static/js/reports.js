import { api } from './api.js';

class ReportsController {
    constructor() {
        this.generateBtn = document.getElementById('generateBtn');
        this.emailInput = document.getElementById('reportEmailInfo');
        this.init();
    }

    init() {
        if (this.generateBtn) this.generateBtn.addEventListener('click', () => this.handleGenerate());
        this.loadRecentReports();
    }

    async handleGenerate() {
        const btn = this.generateBtn;
        const originalText = btn.innerHTML;
        const recipient = this.emailInput ? this.emailInput.value : null;

        btn.disabled = true;
        btn.innerHTML = '<div class="spinner"></div> Generating...';

        try {
            // Include email in options
            const options = {
                date: new Date().toISOString().split('T')[0], // Use today's date for real-time report
                send_email: !!recipient,
                recipient_email: recipient,
                report_type: 'weekly',
                date_range: '7d'
            };

            // Call API
            await api.generateReport(options);

            btn.innerHTML = '<i class="fas fa-check"></i> Complete';
            btn.classList.add('btn-success');

            let msg = "Report generated successfully!";
            if (recipient) msg += ` Emailed to ${recipient}`;

            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('btn-success');
                alert(msg);
            }, 2000);

        } catch (error) {
            console.error(error);
            btn.innerHTML = 'Error';
            btn.disabled = false;
        }
    }

    loadRecentReports() {
        // Logic to fetch list
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ReportsController();
});
