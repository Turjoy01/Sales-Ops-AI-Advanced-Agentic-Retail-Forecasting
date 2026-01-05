
// SECTION NAVIGATION
function switchSection(sectionId, element) {
    // Nav Items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    element.classList.add('active');

    // Section Content
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');

    // Auto-load historical data if switching to history
    if (sectionId === 'history') {
        loadHistory();
    }
}

// FORECAST LOGIC
async function runForecast() {
    const date = document.getElementById('forecastDate').value;
    const btn = document.getElementById('forecastBtn');
    const resultBox = document.getElementById('forecastResult');

    if (!date) {
        alert("Please select a date first.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

    try {
        const response = await fetch('/api/v1/reports/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date, send_email: false })
        });

        if (!response.ok) throw new Error('API Error');

        const data = await response.json();

        resultBox.style.display = 'block';
        document.getElementById('resTitle').innerText = data.date;
        document.getElementById('resVal').innerText = '$' + data.forecast.ensemble_prediction.toLocaleString(undefined, { minimumFractionDigits: 2 });

        const riskLevel = data.risk.risk_level;
        document.getElementById('resTag').innerText = `RISK LEVEL: ${riskLevel}`;
        document.getElementById('resTag').className = `badge badge-${getRiskClass(riskLevel)}`;

        document.getElementById('aiText').innerText = data.explanation;

    } catch (error) {
        console.error(error);
        alert("System error. Ensure FastAPI is running and models are loaded.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Ignite Forecast';
    }
}

// HISTORY LOGIC
async function loadHistory() {
    const tbody = document.getElementById('historyBody');
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 4rem;"><i class="fas fa-spinner fa-spin"></i> Syncing with database...</td></tr>';

    try {
        const response = await fetch('/api/v1/risk/analysis');
        const data = await response.json();

        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 4rem;">No historical records found.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        // Only show first 50 records for performance
        data.slice(0, 50).forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="font-weight: 600;">${row['Order Date']}</td>
                <td>$${parseFloat(row['Sales']).toLocaleString()}</td>
                <td>
                    <span class="badge badge-${getRiskClass(row['risk_level'])}">
                        ${row['risk_score']}%
                    </span>
                </td>
                <td>${row['anomaly_score'] == 1 ? '<i class="fas fa-exclamation-triangle" style="color:var(--accent-red)"></i> Detected' : 'No'}</td>
                <td>${row['reliability'] || 'High'}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (error) {
        console.error(error);
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--accent-red); padding: 4rem;">Failed to fetch history.</td></tr>';
    }
}

// UTILS
function getRiskClass(level) {
    if (!level) return 'success';
    level = level.toLowerCase();
    if (level.includes('low')) return 'success';
    if (level.includes('medium')) return 'warning';
    return 'danger';
}

// On Load
window.onload = () => {
    document.getElementById('forecastDate').value = '2019-01-01';
}
