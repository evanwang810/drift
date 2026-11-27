"""
Enhanced search for knowledge base with faceted search and autocomplete.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Constants
SEARCH_INDEX_PATH = Path(__file__).parent.parent / "docs" / "search_index.json"
HISTORY_LOG_PATH = Path(__file__).parent / "search_history.log"

def load_search_index() -> Dict[str, Any]:
    """Load the search index from JSON file."""
    with open(SEARCH_INDEX_PATH) as f:
        return json.load(f)

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string with fallback support for non-ISO formats."""
    try:
        # Try ISO format first
        return datetime.fromisoformat(date_str)
    except ValueError:
        # Try common non-ISO formats
        # Remove ' UTC' suffix if present
        if date_str.endswith(' UTC'):
            date_str = date_str[:-4]
        
        for fmt in [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y",
        ]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

def filter_by_date(entries: List[Dict[str, Any]], start_date: Optional[str] = None,
                  end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filter entries by date range."""
    filtered = entries
    if start_date:
        start_dt = parse_date(start_date)
        if start_dt:
            filtered = [e for e in filtered if parse_date(e.get('created_at')) >= start_dt]
    if end_date:
        end_dt = parse_date(end_date)
        if end_dt:
            filtered = [e for e in filtered if parse_date(e.get('created_at')) <= end_dt]
    return filtered

def filter_by_type(entries: List[Dict[str, Any]], types: List[str]) -> List[Dict[str, Any]]:
    """Filter entries by type."""
    if not types:
        return entries
    return [e for e in entries if e.get('type') in types]

def filter_by_tag(entries: List[Dict[str, Any]], tags: List[str]) -> List[Dict[str, Any]]:
    """Filter entries by tag."""
    if not tags:
        return entries
    return [e for e in entries if any(tag in e.get('tags', []) for tag in tags)]

def autocomplete(query: str, max_results: int = 10) -> List[str]:
    """Get autocomplete suggestions for a query."""
    index = load_search_index()
    suggestions = set()
    
    for entry in index.get('entries', []):
        title = entry.get('title', '').lower()
        description = entry.get('description', '').lower()
        
        if query.lower() in title:
            suggestions.add(entry.get('title'))
        if query.lower() in description:
            suggestions.add(entry.get('title'))
    
    return sorted(suggestions)[:max_results]

def search(query: str, max_results: int = 10, 
           start_date: Optional[str] = None,
           end_date: Optional[str] = None,
           types: Optional[List[str]] = None,
           tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Search knowledge base with faceted filters.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        start_date: Filter by start date (ISO or common format)
        end_date: Filter by end date (ISO or common format)
        types: Filter by entry types (e.g., ['tool_fix', 'platform'])
        tags: Filter by tags
    
    Returns:
        Dict with 'entries', 'facets', 'total', 'query'
    """
    index = load_search_index()
    all_entries = index.get('entries', [])
    
    # Apply filters
    filtered = all_entries
    filtered = filter_by_date(filtered, start_date, end_date)
    filtered = filter_by_type(filtered, types or [])
    filtered = filter_by_tag(filtered, tags or [])
    
    # Simple relevance scoring (title match = higher score)
    scored = []
    query_lower = query.lower()
    
    for entry in filtered:
        score = 0
        title = entry.get('title', '').lower()
        description = entry.get('description', '').lower()
        
        if query_lower in title:
            score += 10
        if query_lower in description:
            score += 5
        
        scored.append((score, entry))
    
    # Sort by score and return top results
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [entry for score, entry in scored[:max_results]]
    
    # Build facet counts
    facets = {}
    for entry in all_entries:
        # Type facet
        entry_type = entry.get('type')
        facets['type'] = facets.get('type', {})
        facets['type'][entry_type] = facets['type'].get(entry_type, 0) + 1
        
        # Tag facet
        for tag in entry.get('tags', []):
            facets['tag'] = facets.get('tag', {})
            facets['tag'][tag] = facets['tag'].get(tag, 0) + 1
    
    return {
        'entries': results,
        'facets': facets,
        'total': len(results),
        'query': query
    }

def save_search_history(query: str, results: Dict[str, Any]) -> None:
    """Save search query to history log."""
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp}|{query}|{results['total']}\n"
    
    with open(HISTORY_LOG_PATH, 'a') as f:
        f.write(log_entry)

def get_search_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Get recent search history."""
    history = []
    
    if not HISTORY_LOG_PATH.exists():
        return history
    
    with open(HISTORY_LOG_PATH, 'r') as f:
        for line in f:
            if '|' in line:
                timestamp_str, query, count = line.strip().split('|')
                history.append({
                    'timestamp': timestamp_str,
                    'query': query,
                    'count': int(count)
                })
    
    return history[-limit:]

if __name__ == '__main__':
    # Test the search functionality
    print("Testing enhanced search...")
    print(f"Autocomplete for 'search': {autocomplete('search', max_results=5)}")
    
    test_results = search('tool_fix', max_results=5, types=['tool_fix'])
    print(f"\nSearch results for 'tool_fix' (type): {test_results['total']} entries")
    
    test_results = search('date parsing', max_results=5)
    print(f"\nSearch results for 'date parsing': {test_results['total']} entries")
    
    print(f"\nFacets: {test_results['facets']}")
