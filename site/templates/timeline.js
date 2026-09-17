// Load runs data
const runsData = JSON.parse(document.getElementById('runs-json').textContent);

// Render recent runs on the home page
function renderRecentRuns() {
    const container = document.getElementById('run-timeline');
    if (!container) return;

    const recentRuns = runsData.slice(0, 5);

    recentRuns.forEach(run => {
        const outcomeColors = {
            stopped: '#22c55e',
            api_error: '#ef4444',
            crashed: '#f59e0b',
            out_of_turns: '#f59e0b',
            out_of_time: '#8b5cf6'
        };

        const color = outcomeColors[run.outcome] || '#6b7280';

        const runElement = document.createElement('article');
        runElement.className = 'run-item';
        runElement.style.borderLeftColor = color;

        runElement.innerHTML = `
            <div class="run-number" style="color: ${color}">#${run.run}</div>
            <div class="run-info">
                <time>${run.when}</time>
                <div class="run-details">${run.turns} turns, ${run.tokens} tokens</div>
                ${run.note ? `<div class="run-note">${run.note.substring(0, 100)}...</div>` : ''}
            </div>
        `;

        container.appendChild(runElement);
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', renderRecentRuns);
