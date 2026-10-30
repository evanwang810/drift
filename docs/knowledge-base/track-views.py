#!/usr/bin/env python3
"""
Track knowledge base entry views.
Saves view counts to local storage in the browser for the knowledge base page.
"""

import json
import os
import time

# Track views locally for demonstration
# In a real implementation, you would save this to a database

def track_view(entry_id):
    """Track a view of a knowledge base entry."""
    filename = "view_counts.json"
    default_data = {"entries": {}, "last_updated": time.time()}

    # Load existing data
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = default_data

    # Increment view count
    if entry_id not in data["entries"]:
        data["entries"][entry_id] = 0
    data["entries"][entry_id] += 1
    data["last_updated"] = time.time()

    # Save data
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    return data["entries"][entry_id]

def get_view_count(entry_id):
    """Get the view count for an entry."""
    filename = "view_counts.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data.get("entries", {}).get(entry_id, 0)
    return 0

def get_trending_entries(limit=10):
    """Get the most viewed entries."""
    filename = "view_counts.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)

        entries = list(data.get("entries", {}).items())
        # Sort by view count (descending)
        sorted_entries = sorted(entries, key=lambda x: x[1], reverse=True)
        return sorted_entries[:limit]
    return []

if __name__ == "__main__":
    # Test the tracking
    entry_id = "knowledge-entry-1"
    count = track_view(entry_id)
    print(f"Tracked view for {entry_id}: {count} total views")

    # Get trending entries
    trending = get_trending_entries(5)
    print("\nTrending entries:")
    for entry_id, views in trending:
        print(f"  {entry_id}: {views} views")
