// Draw run timeline from runs.json
document.addEventListener('DOMContentLoaded', function() {
    const timeline = document.querySelector('.timeline');
    const colors = {
        'stopped': '#4CAF50',
        'api_error': '#f44336',
        'interrupted': '#ff9800',
        'timed_out': '#9c27b0'
    };

    // Fetch runs from JSON file
    fetch('runs.json')
        .then(response => response.json())
        .then(runs => {
            runs.forEach(run => {
                const runEl = document.createElement('div');
                runEl.className = 'run-item';
                runEl.style.borderLeft = `4px solid ${colors[run.outcome] || '#666'}`;
                
                const date = new Date(run.when);
                const dateStr = date.toLocaleDateString('en-US', { 
                    year: 'numeric', month: 'short', day: 'numeric' 
                });
                
                runEl.innerHTML = `
                    <div class="run-header">
                        <span class="run-number">Run #${run.run}</span>
                        <span class="run-date">${dateStr}</span>
                        <span class="run-outcome">${run.outcome}</span>
                    </div>
                    <div class="run-info">
                        <span>${run.turns} turns</span>
                        <span>${run.tokens.toLocaleString()} tokens</span>
                    </div>
                    <div class="run-note">${run.note}</div>
                `;
                
                runEl.addEventListener('mouseenter', function() {
                    this.querySelector('.run-note').style.display = 'block';
                });
                runEl.addEventListener('mouseleave', function() {
                    this.querySelector('.run-note').style.display = 'none';
                });
                
                timeline.appendChild(runEl);
            });
        })
        .catch(error => {
            console.error('Error loading runs:', error);
            timeline.innerHTML = '<p>Failed to load run data</p>';
        });
});
