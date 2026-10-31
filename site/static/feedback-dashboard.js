// Feedback Dashboard JavaScript
// Load and display feedback analytics

document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});

async function loadDashboard() {
    try {
        // Fetch feedback data
        const response = await fetch('/feedback.json');
        const feedback = await response.json();

        // Update statistics
        updateStats(feedback);

        // Generate charts
        generateCategoryChart(feedback);
        generatePriorityChart(feedback);

        // Display recent feedback
        displayRecentFeedback(feedback);

        // Display alerts
        displayAlerts(feedback);

        // Hide loading, show content
        document.getElementById('dashboard-loading').style.display = 'none';
        document.getElementById('dashboard-content').style.display = 'block';

    } catch (error) {
        console.error('Error loading dashboard:', error);
        document.getElementById('dashboard-loading').style.display = 'none';
        document.getElementById('dashboard-content').innerHTML = '<p>Error loading feedback data.</p>';
    }
}

function updateStats(feedback) {
    const total = feedback.length;
    const critical = feedback.filter(f => f.priority === 'critical').length;
    const high = feedback.filter(f => f.priority === 'high').length;
    const features = feedback.filter(f => f.category === 'feature').length;

    document.getElementById('total-feedback').textContent = total;
    document.getElementById('critical-count').textContent = critical;
    document.getElementById('high-count').textContent = high;
    document.getElementById('feature-count').textContent = features;
}

function generateCategoryChart(feedback) {
    const categories = {};
    feedback.forEach(f => {
        const cat = f.category || 'other';
        categories[cat] = (categories[cat] || 0) + 1;
    });

    const colors = {
        'bug': '#e74c3c',
        'feature': '#3498db',
        'improvement': '#f39c12',
        'compliment': '#2ecc71',
        'other': '#95a5a6'
    };

    let html = '<div class="bar-chart">';
    const total = feedback.length || 1;

    for (const [cat, count] of Object.entries(categories)) {
        const percentage = Math.round((count / total) * 100);
        html += `
            <div class="chart-row">
                <div class="chart-label">${cat}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: ${percentage}%; background-color: ${colors[cat] || '#95a5a6'}"></div>
                </div>
                <div class="chart-value">${count}</div>
            </div>
        `;
    }
    html += '</div>';
    document.getElementById('category-chart').innerHTML = html;
}

function generatePriorityChart(feedback) {
    const priorities = {};
    feedback.forEach(f => {
        const pri = f.priority || 'medium';
        priorities[pri] = (priorities[pri] || 0) + 1;
    });

    const colors = {
        'critical': '#e74c3c',
        'high': '#e67e22',
        'medium': '#f39c12',
        'low': '#2ecc71'
    };

    let html = '<div class="bar-chart">';
    const total = feedback.length || 1;

    for (const [pri, count] of Object.entries(priorities)) {
        const percentage = Math.round((count / total) * 100);
        html += `
            <div class="chart-row">
                <div class="chart-label">${pri}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: ${percentage}%; background-color: ${colors[pri] || '#95a5a6'}"></div>
                </div>
                <div class="chart-value">${count}</div>
            </div>
        `;
    }
    html += '</div>';
    document.getElementById('priority-chart').innerHTML = html;
}

function displayRecentFeedback(feedback) {
    const recent = feedback.slice(0, 10);

    if (recent.length === 0) {
        document.getElementById('recent-feedback').innerHTML = '<p>No feedback data available yet.</p>';
        return;
    }

    const colors = {
        'critical': '#e74c3c',
        'high': '#e67e22',
        'medium': '#f39c12',
        'low': '#2ecc71'
    };

    let html = '<div class="feedback-list">';
    recent.forEach(item => {
        const priorityColor = colors[item.priority] || '#95a5a6';
        html += `
            <div class="feedback-item">
                <div class="feedback-header">
                    <span class="feedback-category">${item.category || 'other'}</span>
                    <span class="feedback-priority" style="color: ${priorityColor}">${item.priority}</span>
                </div>
                <div class="feedback-description">${item.description || 'No description provided'}</div>
                <div class="feedback-meta">
                    <span>${new Date(item.timestamp).toLocaleDateString()}</span>
                    <a href="/feedback.html?feedback_id=${item.id}" class="view-link">View</a>
                </div>
            </div>
        `;
    });
    html += '</div>';
    document.getElementById('recent-feedback').innerHTML = html;
}

function displayAlerts(feedback) {
    const alerts = [];

    // Critical feedback alert
    const critical = feedback.filter(f => f.priority === 'critical');
    if (critical.length > 0) {
        alerts.push({
            type: 'critical',
            message: `⚠️ ${critical.length} critical feedback items require immediate attention`
        });
    }

    // High priority alert
    const high = feedback.filter(f => f.priority === 'high');
    if (high.length > 0) {
        alerts.push({
            type: 'high',
            message: `⚠️ ${high.length} high priority feedback items need review`
        });
    }

    // Bug reports alert
    const bugs = feedback.filter(f => f.category === 'bug');
    if (bugs.length > 0) {
        alerts.push({
            type: 'bug',
            message: `🔍 ${bugs.length} bug reports need investigation`
        });
    }

    // Feature requests alert
    const features = feedback.filter(f => f.category === 'feature');
    if (features.length > 0) {
        alerts.push({
            type: 'feature',
            message: `💡 ${features.length} feature requests pending review`
        });
    }

    if (alerts.length === 0) {
        document.getElementById('alerts-container').innerHTML = '<p>No active alerts.</p>';
        return;
    }

    let html = '<div class="alerts-list">';
    alerts.forEach(alert => {
        html += `<div class="alert alert-${alert.type}">${alert.message}</div>`;
    });
    html += '</div>';
    document.getElementById('alerts-container').innerHTML = html;
}
