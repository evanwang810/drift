"""Backend for feedback collection and management."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "feedback.json"
LOG_FILE = DATA_DIR / "feedback_log.txt"

DATA_FILE = Path("site/data/feedback.json")
LOG_FILE = Path("site/data/feedback_log.txt")

def load_feedback() -> Dict[str, Any]:
    """Load feedback data from JSON file."""
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {
        "submissions": [],
        "summary": {
            "total": 0,
            "by_category": {},
            "by_priority": {},
            "recent": []
        }
    }

def save_feedback(data: Dict[str, Any]) -> None:
    """Save feedback data to JSON file."""
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def log_feedback(submission: Dict[str, Any]) -> None:
    """Log feedback submission to text file."""
    timestamp = datetime.utcnow().isoformat() + " UTC"
    log_entry = f"[{timestamp}] {submission.get('name', 'Anonymous')}: {submission.get('category', 'Unknown')} - {submission.get('priority', 'N/A')}\n"
    LOG_FILE.write_text(log_entry, encoding="utf-8", append=True)

def submit_feedback(submission: Dict[str, Any]) -> Dict[str, Any]:
    """Process and save a feedback submission."""
    data = load_feedback()

    # Add submission
    submission['id'] = len(data['submissions']) + 1
    submission['timestamp'] = datetime.utcnow().isoformat() + " UTC"
    submission['status'] = 'pending'
    submission['responses'] = []

    data['submissions'].append(submission)

    # Update summary
    data['summary']['total'] += 1
    category = submission.get('category', 'unknown')
    priority = submission.get('priority', 'unknown')

    data['summary']['by_category'][category] = data['summary']['by_category'].get(category, 0) + 1
    data['summary']['by_priority'][priority] = data['summary']['by_priority'].get(priority, 0) + 1

    # Add to recent (last 10)
    data['summary']['recent'].insert(0, submission)
    data['summary']['recent'] = data['summary']['recent'][:10]

    save_feedback(data)
    log_feedback(submission)

    return submission

def get_feedback_summary() -> Dict[str, Any]:
    """Get feedback summary statistics."""
    data = load_feedback()
    return data['summary']

def get_feedback_by_id(feedback_id: int) -> Dict[str, Any] | None:
    """Get specific feedback entry by ID."""
    data = load_feedback()
    for submission in data['submissions']:
        if submission.get('id') == feedback_id:
            return submission
    return None

def update_feedback_status(feedback_id: int, status: str, response: str = "") -> bool:
    """Update feedback status and add response."""
    data = load_feedback()
    for submission in data['submissions']:
        if submission.get('id') == feedback_id:
            submission['status'] = status
            submission['responses'].append({
                'timestamp': datetime.utcnow().isoformat() + " UTC",
                'status': status,
                'response': response
            })
            save_feedback(data)
            return True
    return False

def get_high_priority_feedback() -> List[Dict[str, Any]]:
    """Get all high and critical priority feedback."""
    data = load_feedback()
    priority_levels = ['high', 'critical']
    return [s for s in data['submissions'] if s.get('priority') in priority_levels]
