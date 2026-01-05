import { api } from './api.js';

class SettingsController {
    constructor() {
        this.sfSyncBtn = document.getElementById('sfSyncBtn');
        this.gsConnectBtn = document.getElementById('gsConnectBtn');
        this.saveNotifyBtn = document.getElementById('saveNotifyBtn');
        this.regenKeyBtn = document.getElementById('regenKeyBtn');

        this.init();
    }

    init() {
        if (this.sfSyncBtn) this.sfSyncBtn.addEventListener('click', () => this.handleSync());
        if (this.gsConnectBtn) this.gsConnectBtn.addEventListener('click', () => this.handleGoogleConnect());
        if (this.saveNotifyBtn) this.saveNotifyBtn.addEventListener('click', () => this.handleSaveNotify());
        if (this.regenKeyBtn) this.regenKeyBtn.addEventListener('click', () => this.handleRegenKey());

        // Load saved email preferences
        const savedEmails = localStorage.getItem('alertEmails');
        if (savedEmails) {
            document.getElementById('alertEmails').value = savedEmails;
        }
    }

    async handleSync() {
        if (!this.sfSyncBtn) return;

        const btn = this.sfSyncBtn;
        const originalText = btn.innerHTML;

        btn.innerHTML = '<div class="spinner"></div> Syncing...';
        btn.disabled = true;

        try {
            // Default range: 30 days ago to tomorrow
            const end = new Date();
            end.setDate(end.getDate() + 1);
            const start = new Date();
            start.setDate(start.getDate() - 30);

            const result = await api.toggleSalesforceSync({
                start_date: start.toISOString().split('T')[0],
                end_date: end.toISOString().split('T')[0]
            });

            if (result.status === 'success') {
                btn.innerHTML = '<i class="fas fa-check"></i> Synced';
                btn.classList.add('btn-success');
                console.log(`Successfully synced ${result.synced_records} records.`);
            } else {
                throw new Error(result.message || "Sync failed");
            }
        } catch (error) {
            console.error("Salesforce Sync Error:", error);
            btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
            btn.classList.add('btn-danger');
        } finally {
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('btn-success', 'btn-danger');
            }, 3000);
        }
    }

    handleGoogleConnect() {
        if (!this.gsConnectBtn) return;

        const btn = this.gsConnectBtn;
        const status = document.getElementById('gsStatus');

        btn.innerHTML = '<div class="spinner"></div> Connecting...';
        btn.disabled = true;

        // Mock connection for now as requested
        setTimeout(() => {
            btn.disabled = false;
            if (btn.innerText.includes('Connect')) {
                btn.innerHTML = 'Disconnect Account';
                btn.classList.replace('btn-primary', 'btn-danger');
                if (status) {
                    status.innerHTML = '✅ Connected';
                    status.classList.replace('badge-danger', 'badge-success');
                }
                alert("Google Sheets connected successfully (Mock).");
            } else {
                btn.innerHTML = 'Connect Account';
                btn.classList.replace('btn-danger', 'btn-primary');
                if (status) {
                    status.innerHTML = '❌ Disconnected';
                    status.classList.replace('badge-success', 'badge-danger');
                }
            }
        }, 1500);
    }

    handleSaveNotify() {
        const input = document.getElementById('alertEmails');
        const btn = this.saveNotifyBtn;

        if (input.value) {
            localStorage.setItem('alertEmails', input.value);
            btn.innerHTML = '<i class="fas fa-check"></i> Saved';
            setTimeout(() => btn.innerHTML = 'Save Preferences', 2000);
        } else {
            alert("Please enter at least one email.");
        }
    }

    handleRegenKey() {
        if (confirm("Are you sure? This will invalidate the old key.")) {
            const keyField = document.getElementById('apiKeyField');
            keyField.value = 'sk_live_' + Math.random().toString(36).substring(2) + Math.random().toString(36).substring(2);
            alert("New API Key generated.");
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SettingsController();
});
