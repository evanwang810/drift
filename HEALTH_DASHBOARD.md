# Health Dashboard Documentation

## Overview

The repository health dashboard provides real-time visibility into the health status of the drift repository. It displays check results, statistics, and trends to help identify and resolve issues quickly.

## Dashboard Features

### Summary Statistics

The dashboard shows four key metrics:

1. **Total Checks** - Number of health checks being monitored
2. **Passed** - Number of checks that passed
3. **Failed** - Number of checks that failed
4. **Success Rate** - Percentage of checks that passed

### Check List

Individual check results with:
- Pass/fail status indicator (✅/❌)
- Check description
- Color-coded background (green for pass, red for fail)

### Last Run Information

- Timestamp of the most recent health check run
- Date and time in human-readable format

## Implementation Details

### Static HTML

The dashboard is implemented as a static HTML file (`health_dashboard.html`) with embedded CSS and JavaScript.

### JavaScript Data

The dashboard displays static example data for demonstration purposes. In production, this would fetch real data from a health check API.

### Styling

- Responsive design with CSS Grid
- Clean, modern interface
- Mobile-friendly layout
- Accessible color contrast

## Usage

### Viewing the Dashboard

Open `health_dashboard.html` in a web browser to view the current health status.

### Integration

To integrate with real health check data:

1. Create a health check API endpoint that returns JSON
2. Update the JavaScript to fetch data from the endpoint
3. Parse the JSON and update the dashboard dynamically

### Example API Response

```json
{
  "total": 12,
  "passed": 12,
  "failed": 0,
  "rate": "100%",
  "checks": [
    { "passed": true, "message": "index.html exists" },
    { "passed": true, "message": "all 13 posts are linked" }
  ],
  "lastRun": "2026-10-22 00:56 UTC",
  "lastRunTimestamp": "2026-10-22T00:56:00Z"
}
```

## Customization

### Changing the Number of Checks

Edit the `healthData` object in the JavaScript section to include your checks.

### Adding New Metrics

Add new statistic cards in the `.summary` section and update the corresponding JavaScript variables.

### Customizing Colors

Modify the CSS variables or inline styles to change the color scheme.

## Security Considerations

### Data Privacy

- Health check data should not contain sensitive information
- Avoid logging or storing personal data
- Use secure communication (HTTPS) when fetching data

### Access Control

- Restrict access to the dashboard if it contains sensitive metrics
- Consider authentication for internal dashboards

## Maintenance

### Updating Check Data

When health check logic changes, update the dashboard to reflect the new checks.

### Regular Reviews

Review the dashboard monthly to ensure it remains accurate and useful.

## Future Enhancements

Potential improvements:

1. **Real-time updates** - WebSocket or polling for live data
2. **Historical data** - Trends over time, success rate charts
3. **Threshold alerts** - Configure pass/fail thresholds
4. **Notification settings** - User preferences for alert types
5. **Multiple repositories** - Support for monitoring multiple projects
